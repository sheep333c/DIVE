"""
Motifs创建工具。

此工具从序列列表创建motif对象，用于序列模式分析。
"""

from typing import Dict, Any, List
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class MotifsCreateTool(Tool):
    """
    Motifs创建工具。
    
    使用Bio.motifs从序列列表创建motif对象，
    生成共识序列和位置权重矩阵。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        从序列列表创建motif。
        
        Args:
            context: 执行上下文
            params: 参数字典，包含:
                - sequences (List[str]): 序列列表
                - alphabet (str, 可选): 字母表 (默认"ACGT")
        
        Returns:
            motif分析结果
        """
        try:
            from Bio import motifs
            from Bio.Seq import Seq
            
            # 提取参数
            sequences = params.get('sequences', [])
            alphabet = params.get('alphabet', 'ACGT')
            
            # 验证输入
            if not sequences:
                return {"error": "序列列表参数是必需的"}
            
            if not isinstance(sequences, list):
                return {"error": "序列必须是列表格式"}
            
            if len(sequences) < 2:
                return {"error": "至少需要2个序列才能创建motif"}
            
            # 转换为Seq对象
            seq_objects = []
            for seq_str in sequences:
                if not isinstance(seq_str, str):
                    return {"error": "所有序列必须是字符串"}
                seq_objects.append(Seq(seq_str))
            
            # 创建motif
            motif = motifs.create(seq_objects, alphabet=alphabet)
            
            # 直接返回motif的字符串表示
            return str(motif.consensus)
                
        except Exception as e:
            return {"error": str(e)}
