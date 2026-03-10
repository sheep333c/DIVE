"""
Bio.Data.CodonTable遗传密码表工具模块

提供27个遗传密码表的查询功能：
- 标准遗传密码表查询
- 根据ID获取特定密码表
- 所有密码表列表和比较
- 密码子翻译表和起始/终止密码子信息
"""

from .codon_table_standard import CodonTableStandardTool
from .codon_table_by_id import CodonTableByIdTool
from .codon_table_list import CodonTableListTool

__all__ = [
    'CodonTableStandardTool',
    'CodonTableByIdTool',
    'CodonTableListTool'
]