"""
股票筛选模块
根据财务指标和技术指标筛选股票
"""

import pandas as pd
import numpy as np


class StockScreener:
    def __init__(self):
        """初始化股票筛选器"""
        # 存储筛选条件的字典
        # 格式: {
        #     '报表类型': {
        #         '指标名': {
        #             'min_value': 最小值,
        #             'max_value': 最大值
        #         }
        #     }
        # }
        self.filters = {}
        
    def add_filter(self, report_type, indicator_name, min_value=None, max_value=None, allow_null=False):
        """添加筛选条件
        
        Args:
            report_type: str, 报表类型 ('balance'/'income'/'cashflow')
            indicator_name: str, 指标名称
            min_value: float, 最小值 (None表示不设下限)
            max_value: float, 最大值 (None表示不设上限)
            allow_null: bool, 是否允许空值
        """
        if report_type not in self.filters:
            self.filters[report_type] = {}
            
        self.filters[report_type][indicator_name] = {
            'min_value': min_value,
            'max_value': max_value,
            'allow_null': allow_null
        }
    
    def screen(self, df):
        """执行筛选
        
        Args:
            df: DataFrame, 包含股票数据的DataFrame
            
        Returns:
            DataFrame: 符合条件的股票列表
        """
        # 初始化掩码为全True
        mask = pd.Series([True] * len(df), index=df.index)
        
        # 遍历所有筛选条件
        for report_type, indicators in self.filters.items():
            for indicator_name, conditions in indicators.items():
                # 获取指标值
                values = pd.to_numeric(df[indicator_name], errors='coerce')
                
                # 应用最小值过滤
                if conditions['min_value'] is not None:
                    mask &= (values.isna() | (values >= conditions['min_value']))
                
                # 应用最大值过滤
                if conditions['max_value'] is not None:
                    mask &= (values.isna() | (values <= conditions['max_value']))
                
                # 应用空值过滤（如果不允许空值，则排除空值的行）
                if not conditions['allow_null']:
                    mask &= ~values.isna()
        
        # 返回符合条件的股票
        return df[mask][['code(股票代码)', 'stock_name(股票名称)']]
    
    def get_filter_description(self):
        """获取当前的筛选条件描述"""
        descriptions = []
        for report_type, indicators in self.filters.items():
            for indicator, conditions in indicators.items():
                desc = f"{indicator}: "
                if conditions['min_value'] is not None:
                    desc += f"≥ {conditions['min_value']}"
                if conditions['min_value'] is not None and conditions['max_value'] is not None:
                    desc += " 且 "
                if conditions['max_value'] is not None:
                    desc += f"≤ {conditions['max_value']}"
                descriptions.append(desc)
        return descriptions 