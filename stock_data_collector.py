"""
股票数据采集模块
负责从各个数据源获取股票数据
"""

import pandas as pd
import baostock as bs
from datetime import datetime


class StockDataCollector:
    def __init__(self):
        """初始化数据采集器"""
        # 登录系统
        self.bs = bs
        self.login_result = self.bs.login()
        if self.login_result.error_code != '0':
            print(f'登录失败: {self.login_result.error_msg}')
    
    def __del__(self):
        """析构函数，确保退出系统"""
        if hasattr(self, 'bs'):
            self.bs.logout()
        
    def fetch_stock_list(self):
        """获取A股股票列表
        
        Returns:
            pandas.DataFrame: 包含以下字段：
            - code: str, 股票代码
            - code_name: str, 股票名称
            - status: str, 交易状态
            - ipoDate: str, 上市日期
        """
        try:
            # 获取证券基本资料
            rs = self.bs.query_stock_basic()
            if rs.error_code != '0':
                print(f'获取股票列表失败: {rs.error_msg}')
                return pd.DataFrame()
            
            # 转换为DataFrame格式
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            stock_df = pd.DataFrame(data_list, columns=rs.fields)
            
            # 打印字段信息，用于调试
            print("可用的字段：", stock_df.columns.tolist())
            
            # 只保留A股
            stock_df = stock_df[stock_df['type'] == '1']  # 1表示A股
            
            # 整理数据
            result_df = stock_df[[
                'code', 'code_name', 'status', 'ipoDate'
            ]].copy()
            
            # 按照股票代码排序
            result_df = result_df.sort_values('code')
            
            return result_df
            
        except Exception as e:
            print(f"获取股票列表时发生错误：{str(e)}")
            return pd.DataFrame()
    
    def fetch_financial_data(self, stock_code):
        """获取单个股票的财务数据"""
        pass
    
    def fetch_daily_price(self, stock_code):
        """获取股票的日线数据"""
        pass
    
    def fetch_realtime_quote(self, stock_code):
        """获取股票的实时行情"""
        pass 