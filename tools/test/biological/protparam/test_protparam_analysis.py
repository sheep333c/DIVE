"""
测试Bio.SeqUtils.ProtParam蛋白质全面分析工具
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from test.base_verifiable_tool_test import VerifiableToolTestBase
from tools.biological.protparam.protparam_analysis import ProtParamAnalysisTool
from tools.core.types import ExecutionContext
import logging


class TestProtParamAnalysisTool(VerifiableToolTestBase):
    """测试ProtParamAnalysisTool"""
    
    __test__ = True
    TOOL_CLASS_NAME = "ProtParamAnalysisTool"
    
    def get_test_params(self):
        """返回测试参数"""
        return {
            'sequence': 'MAEGEITTFTALTEKFNLPPGNYKKPKLLYCSNGGHFLRILPDGTVDGTRDRSDQHIQLQLSAESVGEVYIKSTETGQYLAMDTSGLLYGSQTPSEECLFLERLEENHYNTYTSKKHAEKNWFVGLKKNGSCKRGPRTHYGQKAILFLPLPV'
        }
    
    def get_tool_instance(self):
        """返回工具实例"""
        return ProtParamAnalysisTool()
    
    def get_execution_context(self):
        """返回执行上下文"""
        return ExecutionContext(
            request_id="test-request",
            logger=logging.getLogger(__name__)
        )


if __name__ == "__main__":
    import unittest
    unittest.main()