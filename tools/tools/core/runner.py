from __future__ import annotations

import json
import os
import time
import uuid
from typing import Any, Dict, Optional

from .registry import Registry


# tool domain/source prefix → env var for optional API key
_AUTH_ENV_MAP = {
    "academic.semantic_scholar.": "SEMANTIC_SCHOLAR_API_KEY",
    "biological.ncbi_entrez.": "NCBI_API_KEY",
}


class StdoutLogger:
    def info(self, msg: str, **kwargs: Any) -> None:
        print(json.dumps({"level": "INFO", "msg": msg, **kwargs}, ensure_ascii=False))

    def warning(self, msg: str, **kwargs: Any) -> None:
        print(json.dumps({"level": "WARN", "msg": msg, **kwargs}, ensure_ascii=False))

    def error(self, msg: str, **kwargs: Any) -> None:
        print(json.dumps({"level": "ERROR", "msg": msg, **kwargs}, ensure_ascii=False))


def run_tool(
    registry: Registry,
    tool_id: str,
    tool_input: Dict[str, Any],
    *,
    timeout_ms: Optional[int] = 15000,
    request_id: Optional[str] = None,
    logger: Optional[StdoutLogger] = None,
) -> str:
    logger = logger or StdoutLogger()
    request_id = request_id or str(uuid.uuid4())
    tool = registry.create_tool(tool_id)
    start = time.time()
    logger.info("tool.start", tool_id=tool_id, request_id=request_id)
    try:
        from .types import ExecutionContext

        # Populate auth from env vars if available
        auth = None
        for prefix, env_var in _AUTH_ENV_MAP.items():
            if tool_id.startswith(prefix):
                key = os.getenv(env_var, "")
                if key:
                    auth = {"api_key": key}
                break

        ctx = ExecutionContext(
            request_id=request_id,
            logger=logger,
            auth=auth,
            timeout_ms=timeout_ms,
        )
        result = tool.execute(ctx, tool_input)
        elapsed_ms = int((time.time() - start) * 1000)
        
        # 将结果转换为字符串
        if result is None:
            result_str = ""
        elif isinstance(result, str):
            result_str = result
        else:
            result_str = json.dumps(result, ensure_ascii=False)
        
        # 智能截断：基于字符数和token数的动态计算
        # 如果是general工具，则不做截断
        if not tool_id.startswith("general"):
            try:
                import tiktoken
                # 如果少于2000字符，直接返回
                if len(result_str) <= 2000:
                    pass
                else:
                    # 计算当前文本的token数和平均字符数
                    encoder = tiktoken.get_encoding("cl100k_base")
                    tokens = encoder.encode(result_str)
                    token_count = len(tokens)
                    
                    # 计算平均每个token的字符数
                    avg_chars_per_token = len(result_str) / token_count
                    
                    # 估算2000 token对应的字符数上限
                    max_chars_for_2000_tokens = int(2000 * avg_chars_per_token)
                    
                    # 如果超过上限，进行截断
                    if len(result_str) > max_chars_for_2000_tokens:
                        result_str = result_str[:max_chars_for_2000_tokens] + "..."
                        
            except ImportError:
                # 如果没有tiktoken，降级到固定字符数截断
                max_length = 4000
                if len(result_str) > max_length:
                    result_str = result_str[:max_length] + "..."
            except Exception:
                # 出错时降级到固定字符数截断
                max_length = 4000
                if len(result_str) > max_length:
                    result_str = result_str[:max_length] + "..."
        
        return result_str 
    
    except Exception as e:
        elapsed_ms = int((time.time() - start) * 1000)
        logger.error("tool.error", tool_id=tool_id, request_id=request_id, elapsed_ms=elapsed_ms, error=str(e))
        return json.dumps({"ok": False, "error": str(e), "meta": {"elapsed_ms": elapsed_ms}}, ensure_ascii=False)