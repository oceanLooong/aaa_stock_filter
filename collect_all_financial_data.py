"""
收集所有股票的财务数据并汇总
"""

from stock_data_collector import StockDataCollector
import pandas as pd
from datetime import datetime
import os
import time

def collect_all_financial_data(year=None, quarter=None):
    # 设置默认的年份和季度
    if year is None:
        year = datetime.now().year
    if quarter is None:
        quarter = (datetime.now().month - 1) // 3 + 1
        
    # 创建数据收集器
    collector = StockDataCollector()
    
    # 获取所有股票列表
    print("获取股票列表...")
    stock_list = collector.fetch_stock_list()
    
    # 只处理状态为1（正常上市）的股票
    active_stocks = stock_list[stock_list['status'] == '1']
    total_stocks = len(active_stocks)
    print(f"共有 {total_stocks} 只正常上市的股票需要处理")
    
    # 创建输出目录
    output_dir = f"financial_data_all_{year}Q{quarter}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 用于存储各类报表数据的列表
    all_data = {
        'profit': [],
        'balance': [],
        'cash_flow': [],
        'indicators': []
    }
    
    # 遍历每只股票获取数据
    for idx, (code, name) in enumerate(zip(active_stocks['code'], active_stocks['code_name']), 1):
        print(f"处理进度: [{idx}/{total_stocks}] {code} {name}")
        
        try:
            # 获取财务数据
            financial_data = collector.fetch_financial_data(code, year, quarter)
            
            # 将数据添加到相应的列表中
            for report_type, df in financial_data.items():
                if not df.empty:
                    # 添加股票名称列
                    df['stock_name'] = name
                    all_data[report_type].append(df)
            
            # 每处理50只股票暂停1秒，避免请求过于频繁
            if idx % 50 == 0:
                time.sleep(1)
                
        except Exception as e:
            print(f"处理 {code} 时出错: {str(e)}")
            continue
    
    # 合并并保存数据
    print("\n保存汇总数据...")
    for report_type, data_list in all_data.items():
        if data_list:
            # 合并同类报表数据
            combined_df = pd.concat(data_list, ignore_index=True)
            
            # 调整列顺序，将股票代码和名称放在前面
            cols = combined_df.columns.tolist()
            cols = ['code', 'stock_name'] + [col for col in cols if col not in ['code', 'stock_name']]
            combined_df = combined_df[cols]
            
            # 保存到CSV文件
            output_file = f"{output_dir}/{report_type}_all.csv"
            combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"已保存{report_type}报表数据，共 {len(combined_df)} 条记录: {output_file}")

if __name__ == "__main__":
    # 收集2024年第3季度的数据
    collect_all_financial_data(2024, 3) 