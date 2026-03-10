"""
Bio.SVDSuperimposer 3D结构叠合分析工具模块

提供3D分子结构叠合分析功能：
- 蛋白质结构比较和叠合
- 原子坐标最优叠合计算
- RMSD计算和结构相似性分析
- 旋转/平移变换矩阵获取
"""

from .svd_superimpose import SvdSuperimposeTool

__all__ = [
    'SvdSuperimposeTool'
]