from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Protocol


class Logger(Protocol):
    def info(self, msg: str, **kwargs: Any) -> None: ...

    def warning(self, msg: str, **kwargs: Any) -> None: ...

    def error(self, msg: str, **kwargs: Any) -> None: ...


@dataclass
class ToolDescriptor:
    id: str
    domain: str
    version: str
    description: str
    auth: Dict[str, Any] = field(default_factory=dict)
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionContext:
    request_id: str
    logger: Logger
    auth: Optional[Dict[str, str]] = None
    timeout_ms: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)


 
 