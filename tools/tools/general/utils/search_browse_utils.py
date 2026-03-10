"""
Search and Browse Utilities
提供搜索和浏览功能的工具函数
"""

import requests
import random
import time
import re
import os
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

# API Keys - 从环境变量读取
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
JINA_API_KEY = os.getenv("JINA_API_KEY", "")
BROWSE_LLM_API_KEY = os.getenv("BROWSE_LLM_API_KEY", "")
BROWSE_LLM_BASE_URL = os.getenv("BROWSE_LLM_BASE_URL", "https://api.deepseek.com")
BROWSE_LLM_MODEL = os.getenv("BROWSE_LLM_MODEL", "deepseek-chat")

# 可选: 使用 tiktoken 进行 token 计数
try:
    import tiktoken
    _tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(text: str) -> int:
        return len(_tokenizer.encode(text))
    
    def truncate_text(text: str, max_tokens: int) -> str:
        tokens = _tokenizer.encode(text)
        if len(tokens) > max_tokens:
            return _tokenizer.decode(tokens[:max_tokens])
        return text

except ImportError:
    # Fallback: 简单的字符估算
    def count_tokens(text: str) -> int:
        return len(text) // 4
    
    def truncate_text(text: str, max_tokens: int) -> str:
        max_chars = max_tokens * 4
        if len(text) > max_chars:
            return text[:max_chars]
        return text


def search_serper(query: str, topk: int = 3) -> list:
    """使用 Serper API 进行 Google 搜索"""
    if not SERPER_API_KEY:
        raise ValueError("SERPER_API_KEY environment variable is not set")
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": topk
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json().get("organic", [])


def search_jina(query: str, topk: int = 3) -> list:
    """使用 Jina AI 进行搜索"""
    if not JINA_API_KEY:
        raise ValueError("JINA_API_KEY environment variable is not set")
    
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "q": query,
        "num": topk
    }
    
    response = requests.post("https://s.jina.ai/", headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json().get("results", [])


def get_brief_text(contents: list) -> str:
    """从搜索结果中提取简要文本"""
    source_text = ""
    for content_json in contents:
        if "extra_snippets" in content_json and len(content_json["extra_snippets"]) > 0:
            snippet = "\n".join(content_json["extra_snippets"])
        elif "snippet" in content_json:
            snippet = content_json["snippet"]
        else:
            snippet = content_json.get("description", "")
        
        url = content_json.get('url', content_json.get('link', ''))
        title = content_json.get('title', '')
        source_text += f"<title>{title}</title>\n<url>{url}</url>\n<snippet>\n{snippet}\n</snippet>\n\n"
    
    return source_text.strip()


def parse_query(query: str) -> tuple:
    """解析搜索查询，提取高级搜索标签"""
    keywords = ["site", "inurl", "intitle", "intext", "inanchor"]
    tag_dict = {key: "" for key in keywords}

    pattern_dict = {"exclude": r'-([^\s]+)', "synonym": r'~([^\s]+)', "exact": r'"([^"]+)"'}
    tag_dict.update({key: set() for key in pattern_dict.keys()})

    # 处理高级搜索关键字
    for keyword in keywords:
        pattern = fr'{keyword}:([^\s]+)'
        match = re.search(pattern, query)
        if match:
            value = match.group(1)
            tag_dict[keyword] = value
            query = re.sub(pattern, '', query).strip()
    
    # 处理其他标签
    for tag, pattern in pattern_dict.items():
        matches = re.findall(pattern, query)
        for match in matches:
            tag_dict[tag].add(match)
        query = re.sub(pattern, '', query).strip()

    # 提取剩余的真正查询内容
    real_query = re.sub(f"[{string.punctuation}]", '', query)

    return tag_dict, real_query


def get_search_results(query: str, topk: int = 3, max_retry: int = 3, engine: str = "serper") -> str:
    """
    获取搜索结果
    
    Args:
        query: 搜索查询
        topk: 返回结果数量
        max_retry: 最大重试次数
        engine: 搜索引擎 ("serper", "jina")
    
    Returns:
        搜索结果文本
    """
    source_text = "Search result is empty. Please try again."
    
    if query.strip() == "":
        return source_text
    
    time.sleep(random.uniform(0, 2))  # 随机延迟避免请求过快
    
    for retry_cnt in range(max_retry):
        try:
            if engine == "jina":
                result = search_jina(query, topk=topk)
            elif engine == "serper":
                result = search_serper(query, topk=topk)
            else:
                raise ValueError(f"Invalid engine: {engine}. Supported: serper, jina")
            
            source_text = get_brief_text(result)
            break
            
        except Exception as e:
            print(f"Search {engine} attempt {retry_cnt + 1} error: {e}", flush=True)
            time.sleep(random.uniform(1, 5))

    if source_text == "" or source_text == "Search result is empty. Please try again.":
        tag_dict, real_query = parse_query(query)
        exact_query = " ".join(list(tag_dict.get("exact", [])))
        real_query = real_query + ", " + exact_query
        real_query = real_query.strip(", ")
        
        if real_query != "" and real_query != query.strip():
            message = f"Search result for query [{query}] is empty. Return search result for cleaned query [{real_query}] instead."
            source_text = get_search_results(real_query, topk=topk, engine=engine)
            if source_text != "" and source_text != "Search result is empty. Please try again.":
                source_text = message + "\n\n" + source_text
        
        if source_text == "":
            print(f"Search {engine} result for query [{query}] is empty", flush=True)
            source_text = "Search result is empty. Please modify the query and try again."
    
    return source_text


def get_search_results_parallel(queries: list, topk: int = 3, max_retry: int = 3, engine: str = "serper") -> str:
    """并行获取多个搜索结果"""
    futures = []
    with ThreadPoolExecutor(max_workers=len(queries)) as executor:
        for i in range(len(queries)):
            futures.append(executor.submit(
                lambda j, q: (j, get_search_results(q, topk=topk, max_retry=max_retry, engine=engine)),
                i, queries[i]
            ))
    
    results = ["" for _ in range(len(queries))]
    for future in as_completed(futures):
        i, output_i = future.result()
        results[i] = output_i
    
    output = ""
    for i, result in enumerate(results):
        output += f"--- search result for [{queries[i]}] ---\n{result}\n--- end of search result ---\n\n"
    
    return output.strip()


def read_url_jina(url: str) -> str:
    """使用 Jina Reader 读取 URL 内容"""
    if not JINA_API_KEY:
        raise ValueError("JINA_API_KEY environment variable is not set")
    
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "X-Engine": "direct",
        "Content-Type": "application/json",
        "X-Retain-Images": "none",
        "X-Return-Format": "markdown",
        "X-Timeout": "60"
    }
    payload = {"url": url}

    response = requests.post("https://r.jina.ai/", headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    return response.text


def read_url_requests(url: str, timeout: int = 30) -> dict:
    """使用 requests 直接读取 URL 内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    
    return {
        "url": url,
        "content": response.text,
        "status_code": response.status_code
    }


def _query_with_llm(content: str, query: str, max_content_tokens: int = 4000) -> str:
    """调用 LLM (OpenAI 兼容格式) 根据网页内容回答问题

    通过环境变量配置:
        BROWSE_LLM_API_KEY:  API key
        BROWSE_LLM_BASE_URL: API base URL (默认 https://api.deepseek.com)
        BROWSE_LLM_MODEL:    模型名 (默认 deepseek-chat)
    """
    if not BROWSE_LLM_API_KEY:
        raise ValueError("BROWSE_LLM_API_KEY environment variable is not set")

    content = truncate_text(content, max_content_tokens)

    payload = {
        "model": BROWSE_LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer the user's question based on the provided webpage content. Be concise and factual. If the content does not contain relevant information, say so.",
            },
            {
                "role": "user",
                "content": f"Webpage content:\n\n{content}\n\nQuestion: {query}",
            },
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
    }
    headers = {
        "Authorization": f"Bearer {BROWSE_LLM_API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        f"{BROWSE_LLM_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def get_browse_results(url: str, query: Optional[str] = None,
                       read_engine: str = "jina", max_retry: int = 3) -> str:
    """
    浏览 URL 并获取内容，若提供 query 则调用 DeepSeek 回答问题

    Args:
        url: 要浏览的 URL
        query: 可选的查询问题
        read_engine: 读取引擎 ("jina", "requests")
        max_retry: 最大重试次数

    Returns:
        URL 内容或 LLM 回答
    """
    time.sleep(random.uniform(0, 2))
    source_text = ""

    for retry_cnt in range(max_retry):
        try:
            if read_engine == "jina":
                source_text = read_url_jina(url)
            elif read_engine == "requests":
                result = read_url_requests(url)
                source_text = result.get("content", "")
            else:
                raise ValueError(f"Invalid read engine: {read_engine}")
            break
        except Exception as e:
            print(f"Read {read_engine} attempt {retry_cnt + 1} error: {e}, url: {url}", flush=True)
            time.sleep(random.uniform(1, 5))

    if source_text.strip() == "":
        print(f"Browse error with empty source_text for url: {url}", flush=True)
        return "Browse error. Please try again."

    if query:
        try:
            answer = _query_with_llm(source_text, query)
            return f"URL: {url}\nQuestion: {query}\nAnswer: {answer}"
        except Exception as e:
            print(f"Browse LLM query failed: {e}, falling back to raw content", flush=True)
            return clip_text(f"Content from {url}:\n\n{source_text}\n\nQuery: {query}")

    return clip_text(source_text)


def clip_text(text: str, max_length: int = 5000) -> str:
    """裁剪文本到指定 token 长度"""
    token_count = count_tokens(text)
    
    if token_count > max_length:
        # 保留前后各一半
        half_length = max_length // 2
        pre_text = truncate_text(text, half_length)
        
        # 从后面截取
        tokens_from_end = count_tokens(text)
        if tokens_from_end > half_length:
            # 简单处理：取最后部分字符
            estimated_chars = half_length * 4
            post_text = text[-estimated_chars:]
        else:
            post_text = text
        
        return "[Tool output is too long, truncated.]\n" + pre_text + "\n...\n" + post_text
    
    return text
