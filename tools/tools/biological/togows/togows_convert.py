"""
TogoWS格式转换工具。

此工具使用TogoWS Web服务进行生物信息学数据格式转换。
"""

from typing import Dict, Any
import time
from tools.core.tool import Tool
from tools.core.types import ExecutionContext


class TogoWSConvertTool(Tool):
    """
    TogoWS格式转换工具。
    
    使用Bio.TogoWS在不同生物信息学数据格式之间进行转换。
    支持多种格式如FASTA、GenBank、GFF等。
    """
    
    def execute(self, context: ExecutionContext, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行TogoWS格式转换。
        
        Args:
            context: 执行上下文
            params: 参数字典，包含:
                - data (str): 要转换的输入数据
                - input_format (str): 输入格式 (如 "fasta", "genbank")
                - output_format (str): 输出格式 (如 "gff", "fasta")
        
        Returns:
            包含转换结果的字典
        """
        try:
            from Bio import TogoWS
            
            # 提取参数
            data = params.get('data', '')
            input_format = params.get('input_format', '')
            output_format = params.get('output_format', '')
            
            # 验证输入
            if not data:
                return {"error": "数据参数是必需的"}
            
            if not input_format:
                return {"error": "输入格式参数是必需的"}
            
            if not output_format:
                return {"error": "输出格式参数是必需的"}
            
            if input_format == output_format:
                return {"error": "输入格式和输出格式不能相同"}
            
            # 执行带重试机制的请求
            max_retries = 3
            retry_delay = 1.0
            
            for attempt in range(max_retries):
                try:
                    # 调用TogoWS格式转换
                    with TogoWS.convert(data, input_format, output_format) as handle:
                        return handle.read()
                    
                except Exception as retry_e:
                    error_msg = str(retry_e)
                    
                    # 检查是否是不支持的转换
                    if "Unsupported conversion" in error_msg:
                        return {"error": error_msg}
                    
                    if attempt < max_retries - 1:
                        if "timeout" in error_msg.lower() or "URLError" in error_msg:
                            time.sleep(retry_delay * (attempt + 1))
                            continue
                    raise retry_e
            return {"error": "Max retries exceeded"}
                
        except Exception as e:
            return {"error": str(e)}
