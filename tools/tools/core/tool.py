from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from .types import ExecutionContext, ToolDescriptor


class Tool(ABC):
    descriptor: ToolDescriptor

    @abstractmethod
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Any:
        raise NotImplementedError


 
 