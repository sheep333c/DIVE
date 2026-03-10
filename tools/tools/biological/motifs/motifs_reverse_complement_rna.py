"""
Motifs RNA反向互补工具。

此工具计算RNA序列的反向互补序列。
"""

from typing import Dict, Any
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class MotifsReverseComplementRnaTool(Tool):
    """
    Motifs RNA反向互补工具。
    
    使用Bio.motifs计算RNA序列的反向互补序列。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算RNA序列的反向互补。
        
        Args:
            context: 执行上下文
            params: 参数字典，包含:
                - sequence (str): RNA序列
                - inplace (bool, 可选): 是否就地修改 (默认False)
        
        Returns:
            反向互补序列
        """
        try:
            from Bio import motifs
            from Bio.Seq import Seq
            
            # 提取参数
            sequence = params.get('sequence', '')
            inplace = params.get('inplace', False)
            
            # 验证输入
            if not sequence:
                return {"error": "序列参数是必需的"}
            
            # 转换为Seq对象
            seq_obj = Seq(sequence)
            
            # 计算RNA反向互补
            result = motifs.reverse_complement_rna(seq_obj, inplace=inplace)
            
            # 直接返回序列字符串
            return str(result)
                
        except Exception as e:
            return {"error": str(e)}
