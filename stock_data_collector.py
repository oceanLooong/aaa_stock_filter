"""
股票数据采集模块
负责从各个数据源获取股票数据
"""

import pandas as pd
import baostock as bs
from datetime import datetime, timedelta


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
    
    def fetch_financial_data(self, stock_code, year=None, quarter=None):
        """获取单个股票的财务数据
        
        Args:
            stock_code: str, 股票代码（如：sh.600000）
            year: int, 年份（如：2023），默认为最新年份
            quarter: int, 季度（1-4），默认为最新季度
            
        Returns:
            dict: 包含以下DataFrame：
            - profit: 利润表
            - balance: 资产负债表
            - cash_flow: 现金流量表
            - indicators: 财务指标
        """
        try:
            if year is None:
                year = datetime.now().year
            if quarter is None:
                quarter = (datetime.now().month - 1) // 3 + 1
                
            result = {}
            
            # 1. 获取利润表
            profit_rs = self.bs.query_profit_data(code=stock_code, year=year, quarter=quarter)
            if profit_rs.error_code == '0':
                profit_list = []
                while (profit_rs.error_code == '0') & profit_rs.next():
                    profit_list.append(profit_rs.get_row_data())
                result['profit'] = pd.DataFrame(profit_list, columns=profit_rs.fields)
            
            # 2. 获取资产负债表
            balance_rs = self.bs.query_balance_data(code=stock_code, year=year, quarter=quarter)
            if balance_rs.error_code == '0':
                balance_list = []
                while (balance_rs.error_code == '0') & balance_rs.next():
                    balance_list.append(balance_rs.get_row_data())
                result['balance'] = pd.DataFrame(balance_list, columns=balance_rs.fields)
            
            # 3. 获取现金流量表
            cash_flow_rs = self.bs.query_cash_flow_data(code=stock_code, year=year, quarter=quarter)
            if cash_flow_rs.error_code == '0':
                cash_flow_list = []
                while (cash_flow_rs.error_code == '0') & cash_flow_rs.next():
                    cash_flow_list.append(cash_flow_rs.get_row_data())
                result['cash_flow'] = pd.DataFrame(cash_flow_list, columns=cash_flow_rs.fields)
            
            # 4. 获取主要财务指标
            indicators_rs = self.bs.query_dupont_data(code=stock_code, year=year, quarter=quarter)
            if indicators_rs.error_code == '0':
                indicators_list = []
                while (indicators_rs.error_code == '0') & indicators_rs.next():
                    indicators_list.append(indicators_rs.get_row_data())
                result['indicators'] = pd.DataFrame(indicators_list, columns=indicators_rs.fields)
            
            return result
            
        except Exception as e:
            print(f"获取财务数据时发生错误：{str(e)}")
            return {}
    
    def fetch_valuation_data(self, stock_code):
        """获取单个股票的估值数据
        
        Args:
            stock_code: str, 股票代码 (如："sh.600000")
            
        Returns:
            dict: 包含以下字段：
            - pe_ttm: float, 市盈率TTM
            - pb: float, 市净率
            - ps: float, 市销率
            - price: float, 当前价格
            - volume: float, 成交量
            - amount: float, 成交额
            - turnover: float, 换手率
        """
        try:
            # 获取当前日期
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 获取基本面数据
            rs = self.bs.query_stock_basic(code=stock_code)
            if rs.error_code != '0':
                print(f'获取{stock_code}基本信息失败: {rs.error_msg}')
                return None
            
            # 获取当日行情数据    
            rs_k = self.bs.query_history_k_data_plus(
                code=stock_code,
                fields="date,code,close,volume,amount,turn",
                start_date=today,
                end_date=today,
                frequency="d",
                adjustflag="3"
            )
            
            result = {}
            
            # 解析基本面数据
            if rs.error_code == '0' and rs.next():
                basic_info = rs.get_row_data()
                # 注意：字段索引可能需要根据实际API返回调整
                result['pe_ttm'] = float(basic_info[15]) if len(basic_info) > 15 and basic_info[15] != '' else None
                result['pb'] = float(basic_info[16]) if len(basic_info) > 16 and basic_info[16] != '' else None
            
            # 解析行情数据
            if rs_k.error_code == '0' and rs_k.next():
                k_data = rs_k.get_row_data()
                result['price'] = float(k_data[2]) if k_data[2] != '' else None
                result['volume'] = float(k_data[3]) if k_data[3] != '' else None
                result['amount'] = float(k_data[4]) if k_data[4] != '' else None
                result['turnover'] = float(k_data[5]) if k_data[5] != '' else None
            
            return result
            
        except Exception as e:
            print(f"获取{stock_code}估值数据时发生错误：{str(e)}")
            return None
    
    def fetch_daily_price(self, stock_code):
        """获取股票的日线数据"""
        pass
    
    def fetch_realtime_quote(self, stock_code):
        """获取股票的实时行情"""
        pass 