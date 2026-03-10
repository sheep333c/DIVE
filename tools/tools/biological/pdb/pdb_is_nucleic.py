"""
PDB核酸识别工具。

此工具判断给定的残基是否为核酸。
"""

from typing import Dict, Any
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class PdbIsNucleicTool(Tool):
    """
    PDB核酸识别工具。
    
    使用Bio.PDB判断残基是否为核酸，
    支持标准和非标准核酸识别。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        判断残基是否为核酸。
        
        Args:
            context: 执行上下文
            params: 参数字典，包含:
                - residue (str): 残基名称或代码
                - standard (bool, 可选): 是否只检查标准核酸 (默认False)
        
        Returns:
            布尔值结果
        """
        try:
            from Bio.PDB import is_nucleic
            
            # 提取参数
            residue = params.get('residue', '')
            standard = params.get('standard', False)
            
            # 验证输入
            if not residue:
                return {"error": "残基参数是必需的"}
            
            # 执行带重试机制的请求
            max_retries = 2
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    # 调用Bio.PDB函数
                    result = is_nucleic(residue, standard=standard)
                    
                    # 直接返回布尔值
                    return result
                    
                except Exception as retry_e:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                    raise retry_e
            return {"error": "Max retries exceeded"}
                
        except Exception as e:
            return {"error": str(e)}
