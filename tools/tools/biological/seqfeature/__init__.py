"""
Bio.SeqFeature序列特征工具模块

提供序列特征和位置分析功能：
- 序列特征位置创建和管理
- 单一位置和复合位置处理
- 序列片段提取和分析
- 基因注释和特征定位
"""

from .seqfeature_location import SeqFeatureLocationTool
from .seqfeature_compound import SeqFeatureCompoundTool

__all__ = [
    'SeqFeatureLocationTool',
    'SeqFeatureCompoundTool'
]