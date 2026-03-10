"""
Bio.Data.IUPACData分子量数据查询工具
获取DNA、RNA、蛋白质的分子量数据
"""

import time
import os
import json
from typing import Dict, Any
from Bio.Data import IUPACData
from tools.core.tool import Tool


class IupacDataWeightsTool(Tool):
    """IUPAC分子量数据查询工具"""

    def execute(self, context, params: Dict[str, Any]):
        """
        获取IUPAC分子量数据
        
        参数:
        - sequence_type: 序列类型 ('dna', 'rna', 'protein', 'all')，默认'all'
        - weight_type: 分子量类型 ('monoisotopic', 'average', 'both')，默认'both'
        """
        max_retries = 2
        retry_delay = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # 提取参数
                sequence_type = params.get('sequence_type', 'all').lower()
                weight_type = params.get('weight_type', 'both').lower()
                
                result = {}
                
                # DNA分子量
                if sequence_type in ['dna', 'all']:
                    dna_weights = {}
                    
                    if weight_type in ['monoisotopic', 'both']:
                        dna_weights['monoisotopic'] = dict(IUPACData.monoisotopic_unambiguous_dna_weights)
                    
                    if weight_type in ['average', 'both']:
                        dna_weights['average'] = dict(IUPACData.avg_ambiguous_dna_weights)
                        dna_weights['unambiguous_average'] = dict(IUPACData.unambiguous_dna_weights)
                        dna_weights['weight_ranges'] = dict(IUPACData.unambiguous_dna_weight_ranges)
                        dna_weights['ambiguous_weight_ranges'] = dict(IUPACData.ambiguous_dna_weight_ranges)
                    
                    result['dna'] = dna_weights
                
                # RNA分子量
                if sequence_type in ['rna', 'all']:
                    rna_weights = {}
                    
                    if weight_type in ['monoisotopic', 'both']:
                        rna_weights['monoisotopic'] = dict(IUPACData.monoisotopic_unambiguous_rna_weights)
                    
                    if weight_type in ['average', 'both']:
                        rna_weights['average'] = dict(IUPACData.avg_ambiguous_rna_weights)
                        rna_weights['unambiguous_average'] = dict(IUPACData.unambiguous_rna_weights)
                        rna_weights['weight_ranges'] = dict(IUPACData.unambiguous_rna_weight_ranges)
                        rna_weights['ambiguous_weight_ranges'] = dict(IUPACData.ambiguous_rna_weight_ranges)
                    
                    result['rna'] = rna_weights
                
                # 蛋白质分子量
                if sequence_type in ['protein', 'all']:
                    protein_weights = {}
                    
                    if weight_type in ['monoisotopic', 'both']:
                        protein_weights['monoisotopic'] = dict(IUPACData.monoisotopic_protein_weights)
                    
                    if weight_type in ['average', 'both']:
                        protein_weights['average'] = dict(IUPACData.protein_weights)
                        protein_weights['extended_average'] = dict(IUPACData.avg_extended_protein_weights)
                        protein_weights['weight_ranges'] = dict(IUPACData.protein_weight_ranges)
                        protein_weights['extended_weight_ranges'] = dict(IUPACData.extended_protein_weight_ranges)
                    
                    result['protein'] = protein_weights
                
                # 原子分子量
                if sequence_type == 'all':
                    result['atoms'] = dict(IUPACData.atom_weights)
                
                return result
                
            except Exception as e:
                if attempt == max_retries:
                    return {"error": f"获取IUPAC分子量数据失败: {str(e)}"}
                time.sleep(retry_delay)
                retry_delay *= 2
        return {"error": "Max retries exceeded"}
