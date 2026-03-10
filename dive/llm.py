#!/usr/bin/env python3
"""LLM API client — pure API communication layer.

Internal message format: OpenAI standard.
- OpenAI-compatible path: zero conversion via openai SDK.
- Anthropic path: boundary conversion OpenAI <-> Anthropic.

Tool execution is delegated to ToolRunner (dependency injection).
"""

import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import anthropic
import openai

from .tool_runner import ToolRunner


class LLMClient:
    """LLM API client — supports Anthropic native and OpenAI-compatible providers."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        tool_config: Optional[Dict] = None,
        save_json: bool = True,
        json_save_dir: str = "json_responses",
        enable_cache: bool = True,
        provider: Optional[str] = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 16384,
        timeout: int = 300,
        tool_runner: Optional[ToolRunner] = None,
    ):
        self.provider = (provider or os.getenv("LLM_PROVIDER", "anthropic")).strip().lower()
        valid_providers = ["anthropic", "openai_compatible"]
        if self.provider not in valid_providers:
            raise ValueError(f"Invalid provider: {self.provider}. Valid options: {valid_providers}")

        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key is required. Please provide api_key parameter or "
                "set ANTHROPIC_API_KEY / OPENAI_API_KEY environment variable."
            )

        self.client = None
        self.openai_client = None
        if self.provider == "anthropic":
            resolved_url = base_url or os.getenv("ANTHROPIC_BASE_URL")
            if resolved_url:
                resolved_url = resolved_url.rstrip("/")
                for suffix in ["/v1/messages", "/messages", "/v1"]:
                    if resolved_url.endswith(suffix):
                        resolved_url = resolved_url[: -len(suffix)]
                        break
                self.client = anthropic.Anthropic(api_key=self.api_key, base_url=resolved_url)
                print(f"Using Anthropic endpoint: {resolved_url}")
            else:
                self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            resolved_url = base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1"
            resolved_url = resolved_url.rstrip("/")
            if resolved_url.endswith("/chat/completions"):
                resolved_url = resolved_url[: -len("/chat/completions")]
            if not resolved_url.endswith("/v1"):
                resolved_url = f"{resolved_url}/v1"
            self.openai_client = openai.OpenAI(
                api_key=self.api_key, base_url=resolved_url, timeout=timeout,
            )
            print(f"Using OpenAI-compatible endpoint: {resolved_url}")

        self.model = model
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.tool_config = tool_config or {}

        # Cache only works with Anthropic provider
        if self.provider != "anthropic":
            self.enable_cache = False
        else:
            self.enable_cache = enable_cache

        self.save_json = save_json
        self.json_save_dir = json_save_dir
        self.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.round_counter = 0

        if self.save_json:
            os.makedirs(self.json_save_dir, exist_ok=True)

        self.conversation_history: List[Dict[str, Any]] = []
        self.content_stats = {
            "thinking_blocks": 0,
            "text_blocks": 0,
            "tool_use_blocks": 0,
            "redacted_thinking_blocks": 0,
        }

        # Tool execution via injected ToolRunner
        self.tool_runner = tool_runner

    # ------------------------------------------------------------------
    # JSON save helper
    # ------------------------------------------------------------------

    def _save_json_response(self, request_data: Dict, response_data: Dict, round_num: int):
        if not self.save_json:
            return
        save_data = {
            "conversation_id": self.conversation_id,
            "round": round_num,
            "timestamp": datetime.now().isoformat(),
            "request": request_data,
            "response": response_data,
        }
        filename = f"{self.json_save_dir}/claude_round_{round_num:02d}_{self.conversation_id}.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _update_content_stats(self, assistant_msg: Dict[str, Any]) -> None:
        if assistant_msg.get("reasoning_content"):
            self.content_stats["thinking_blocks"] += 1
        if assistant_msg.get("content"):
            self.content_stats["text_blocks"] += 1
        tc = assistant_msg.get("tool_calls") or []
        self.content_stats["tool_use_blocks"] += len(tc)

    # ------------------------------------------------------------------
    # Anthropic cache helpers (operate on Anthropic-format messages)
    # ------------------------------------------------------------------

    def _add_cache_control_to_content(self, content: Any) -> None:
        if self.enable_cache:
            if isinstance(content, dict):
                content["cache_control"] = {"type": "ephemeral"}
            elif isinstance(content, list) and content:
                if isinstance(content[-1], dict):
                    content[-1]["cache_control"] = {"type": "ephemeral"}

    def _add_cache_control_to_messages(self, messages: List[Dict]) -> List[Dict]:
        """Add cache control to the last user message. Operates on Anthropic-format messages."""
        if not self.enable_cache or not messages:
            return messages
        for i in range(len(messages) - 1, -1, -1):
            message = messages[i]
            if message.get("role") == "user":
                content = message.get("content")
                if isinstance(content, list) and content:
                    self._add_cache_control_to_content(content)
                elif isinstance(content, str):
                    message["content"] = [
                        {"type": "text", "text": content, "cache_control": {"type": "ephemeral"}}
                    ]
                break
        return messages

    def _add_cache_control_to_tools(self, tools: List[Dict]) -> List[Dict]:
        if not self.enable_cache or not tools:
            return tools
        if tools:
            tools[-1]["cache_control"] = {"type": "ephemeral"}
        return tools

    # ------------------------------------------------------------------
    # Anthropic <-> OpenAI format conversion
    # ------------------------------------------------------------------

    def _convert_messages_to_anthropic(self, messages: List[Dict]) -> List[Dict]:
        """Convert OpenAI-format messages to Anthropic-format messages."""
        anthropic_messages: List[Dict] = []
        for msg in messages:
            role = msg.get("role")

            if role == "user":
                anthropic_messages.append({"role": "user", "content": msg.get("content", "")})

            elif role == "assistant":
                # Use preserved raw Anthropic content if available (lossless round-trip)
                raw = msg.get("_anthropic_content")
                if raw:
                    anthropic_messages.append({"role": "assistant", "content": raw})
                else:
                    # Reconstruct from OpenAI fields (for messages from OpenAI-compatible path)
                    content_blocks: List[Dict] = []
                    if msg.get("reasoning_content"):
                        content_blocks.append({"type": "thinking", "thinking": msg["reasoning_content"]})
                    if msg.get("content"):
                        content_blocks.append({"type": "text", "text": msg["content"]})
                    for tc in msg.get("tool_calls") or []:
                        fn = tc.get("function", {})
                        raw_args = fn.get("arguments", "{}")
                        try:
                            parsed = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                        except (json.JSONDecodeError, TypeError):
                            parsed = {"raw_arguments": raw_args}
                        content_blocks.append({
                            "type": "tool_use",
                            "id": tc.get("id"),
                            "name": fn.get("name"),
                            "input": parsed,
                        })
                    if not content_blocks:
                        content_blocks.append({"type": "text", "text": ""})
                    anthropic_messages.append({"role": "assistant", "content": content_blocks})

            elif role == "tool":
                tool_result = {
                    "type": "tool_result",
                    "tool_use_id": msg.get("tool_call_id"),
                    "content": msg.get("content", ""),
                }
                # Merge consecutive tool results into one user message
                if (
                    anthropic_messages
                    and anthropic_messages[-1].get("role") == "user"
                    and isinstance(anthropic_messages[-1].get("content"), list)
                ):
                    anthropic_messages[-1]["content"].append(tool_result)
                else:
                    anthropic_messages.append({"role": "user", "content": [tool_result]})

        return anthropic_messages

    def _normalize_anthropic_response(self, response_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Anthropic response dict to OpenAI-format assistant message."""
        content_blocks = response_dict.get("content", [])

        text_parts: List[str] = []
        tool_calls: List[Dict] = []
        reasoning_parts: List[str] = []

        for block in content_blocks:
            bt = block.get("type", "")
            if bt == "text":
                text_parts.append(block.get("text", ""))
            elif bt == "tool_use":
                tool_calls.append({
                    "id": block.get("id"),
                    "type": "function",
                    "function": {
                        "name": block.get("name"),
                        "arguments": json.dumps(block.get("input", {}), ensure_ascii=False),
                    },
                })
            elif bt == "thinking":
                reasoning_parts.append(block.get("thinking", ""))
            elif bt == "redacted_thinking":
                self.content_stats["redacted_thinking_blocks"] += 1

        msg: Dict[str, Any] = {
            "role": "assistant",
            "content": "\n".join(text_parts) if text_parts else None,
            # Preserve raw Anthropic content for lossless round-tripping
            # (redacted_thinking, interleaved block order, etc.)
            "_anthropic_content": content_blocks,
        }
        if tool_calls:
            msg["tool_calls"] = tool_calls
        if reasoning_parts:
            msg["reasoning_content"] = "\n\n".join(reasoning_parts)

        return msg

    # ------------------------------------------------------------------
    # API calls
    # ------------------------------------------------------------------

    def _call_claude_api(
        self,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.0,
        max_retries: int = 8,
    ) -> Dict[str, Any]:
        """Call the LLM API. Returns assistant message in OpenAI format."""
        if self.provider == "openai_compatible":
            return self._call_openai_compatible_api(messages, tools, temperature, max_retries)

        # --- Anthropic path: convert messages at boundary, tools are already native ---
        anthropic_messages = self._convert_messages_to_anthropic(messages)
        anthropic_tools = tools  # already Anthropic-native from _get_tool_schemas

        if self.enable_cache:
            anthropic_messages = self._add_cache_control_to_messages(anthropic_messages)
            if anthropic_tools:
                anthropic_tools = self._add_cache_control_to_tools(anthropic_tools)

        request_params: Dict[str, Any] = {
            "model": self.model,
            "messages": anthropic_messages,
            "max_tokens": self.max_tokens,
            # Anthropic requires temperature=1 when thinking is enabled;
            # caller-specified temperature is intentionally ignored here.
            "temperature": 1.0,
        }

        thinking_budget = min(32768, self.max_tokens - 4096)
        request_params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}

        if anthropic_tools:
            request_params["tools"] = anthropic_tools

        extra_headers = {"anthropic-beta": "interleaved-thinking-2025-05-14"}

        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                response = self.client.messages.create(
                    **request_params,
                    extra_headers=extra_headers if extra_headers else None,
                    timeout=self.timeout,
                )
                response_dict = {
                    "id": response.id,
                    "type": response.type,
                    "role": response.role,
                    "content": [block.model_dump() for block in response.content],
                    "model": response.model,
                    "stop_reason": response.stop_reason,
                    "stop_sequence": response.stop_sequence,
                    "usage": response.usage.model_dump() if response.usage else None,
                }
                self.round_counter += 1
                self._save_json_response(request_params, response_dict, self.round_counter)

                # Normalize to OpenAI format
                return self._normalize_anthropic_response(response_dict)

            except anthropic.RateLimitError:
                print("\u26a0\ufe0f Rate limit hit, sleeping 60s...")
                time.sleep(60)
                continue
            except anthropic.APIStatusError as e:
                if e.status_code in [503, 502, 504]:
                    if attempt < max_retries:
                        time.sleep(min(60, (2 ** attempt) * 5))
                        continue
                    raise Exception(f"API call failed after {max_retries} retries: {e.status_code}")
                elif e.status_code in [400, 401, 403, 404]:
                    raise Exception(f"Client error, check request format: {e.status_code}")
                else:
                    if attempt < max_retries:
                        time.sleep(min(30, (2 ** attempt) * 5))
                        continue
                    raise Exception(f"API call failed after {max_retries} retries: {e.status_code}")
            except anthropic.APITimeoutError as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(min(20, (2 ** attempt) * 5))
                    continue
                raise Exception(f"API call timed out after {max_retries} retries")
            except anthropic.APIConnectionError as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(min(25, (2 ** attempt) * 6))
                    continue
                raise Exception(f"API connection failed after {max_retries} retries")
            except Exception as e:
                raise e

        if last_exception:
            raise Exception(f"API call failed after {max_retries} retries, last exception: {last_exception}")
        raise Exception(f"API call failed after {max_retries} retries")

    # ------------------------------------------------------------------
    # OpenAI compatible (via openai SDK — zero conversion)
    # ------------------------------------------------------------------

    def _call_openai_compatible_api(
        self,
        messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.0,
        max_retries: int = 8,
    ) -> Dict[str, Any]:
        """Call OpenAI-compatible API via openai SDK. Returns assistant message in OpenAI format."""
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = self._tools_to_openai(tools)
            kwargs["tool_choice"] = "auto"

        # Gemini: request thinking/reasoning content via extra_body
        if "gemini" in self.model.lower():
            kwargs["extra_body"] = {
                "google": {"thinking_config": {"include_thoughts": True}}
            }

        last_exception = None
        for attempt in range(max_retries + 1):
            try:
                response = self.openai_client.chat.completions.create(**kwargs)
                choice = response.choices[0]
                message = choice.message

                result: Dict[str, Any] = {
                    "role": "assistant",
                    "content": message.content,
                }
                if message.tool_calls:
                    result["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in message.tool_calls
                    ]
                reasoning = getattr(message, "reasoning_content", None) or getattr(message, "reasoning", None)
                if reasoning:
                    result["reasoning_content"] = reasoning

                self.round_counter += 1
                self._save_json_response(kwargs, response.model_dump(), self.round_counter)
                return result

            except openai.RateLimitError:
                last_exception = Exception("Rate limit exceeded")
                if attempt < max_retries:
                    time.sleep(min(60, (2 ** attempt) * 5))
                    continue
                raise Exception(f"OpenAI-compatible API rate limit after {max_retries} retries")
            except openai.APIStatusError as e:
                last_exception = e
                if e.status_code in [429, 503, 502, 504] and attempt < max_retries:
                    time.sleep(min(60, (2 ** attempt) * 5))
                    continue
                raise Exception(f"OpenAI-compatible API call failed: {e.status_code}")
            except openai.APITimeoutError as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(min(20, (2 ** attempt) * 5))
                    continue
                raise Exception(f"API call timed out after {max_retries} retries")
            except openai.APIConnectionError as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(min(25, (2 ** attempt) * 6))
                    continue
                raise Exception(f"API connection failed after {max_retries} retries")
            except Exception as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(min(20, (2 ** attempt) * 5))
                    continue
                raise e

        raise Exception(f"OpenAI-compatible API call failed after {max_retries} retries: {last_exception}")

    # ------------------------------------------------------------------
    # Chat with tools
    # ------------------------------------------------------------------

    def chat_with_tools(
        self,
        user_query: str,
        tool_names: Optional[List[str]] = None,
        max_rounds: int = 5,
        temperature: float = 1.0,
        reset_history: bool = False,
        set_json_save_dir: Optional[str] = None,
        max_retries: int = 8,
    ) -> str:
        if reset_history:
            self.reset_conversation()
        if set_json_save_dir:
            self.json_save_dir = set_json_save_dir

        tools = self._get_tool_schemas(tool_names) if tool_names else None

        if not self.conversation_history:
            messages = [{"role": "user", "content": user_query}]
        else:
            messages = self.conversation_history + [{"role": "user", "content": user_query}]

        round_count = 0
        while round_count < max_rounds:
            round_count += 1
            assistant_msg = self._call_claude_api(messages, tools, temperature, max_retries)

            self._update_content_stats(assistant_msg)
            messages.append(assistant_msg)

            tool_calls = assistant_msg.get("tool_calls")
            if tool_calls:
                for tc in tool_calls:
                    result = self._execute_tool(tc)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": result,
                    })
            else:
                self.conversation_history = messages
                return assistant_msg.get("content") or ""

        self.conversation_history = messages
        return "Conversation reached maximum round limit"

    def _get_tool_schemas(self, tool_names: List[str]) -> List[Dict]:
        """Get tool schemas in Anthropic-native format — delegates to ToolRunner."""
        if self.tool_runner:
            return self.tool_runner.get_tool_schemas(tool_names)
        return []

    @staticmethod
    def _tools_to_openai(tools: List[Dict]) -> List[Dict]:
        """Convert Anthropic-native tool schemas to OpenAI format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "parameters": t.get("input_schema", {"type": "object", "properties": {}}),
                },
            }
            for t in tools
        ]

    def _execute_tool(self, tool_call: Dict) -> str:
        """Execute a tool from OpenAI-format tool_call — delegates to ToolRunner."""
        if self.tool_runner:
            try:
                fn = tool_call.get("function", {})
                name = fn.get("name")
                raw_args = fn.get("arguments", "{}")
                try:
                    args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                except (json.JSONDecodeError, TypeError):
                    args = {}
                return self.tool_runner.execute(name, args)
            except Exception as e:
                return f"Tool execution failed: {e}"
        return "Tool execution failed: no tool_runner configured"

    # ------------------------------------------------------------------
    # Conversation management
    # ------------------------------------------------------------------

    def get_conversation_summary(self) -> Dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "total_rounds": self.round_counter,
            "history_length": len(self.conversation_history),
            "content_statistics": self.content_stats.copy(),
        }

    def set_conversation_history(self, conversation_history: List[Dict]):
        self.conversation_history = conversation_history

    def set_round_counter(self, round_counter: int):
        self.round_counter = round_counter

    def reset_conversation(self):
        self.conversation_history = []
        self.round_counter = 0
        self.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.content_stats = {
            "thinking_blocks": 0,
            "text_blocks": 0,
            "tool_use_blocks": 0,
            "redacted_thinking_blocks": 0,
        }

    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history.copy()

    def clear_conversation_history(self):
        self.conversation_history.clear()
