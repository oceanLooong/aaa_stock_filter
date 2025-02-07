from stock_data_collector import StockDataCollector
import pandas as pd
import os

def test_fetch_stock_list():
    # 创建收集器实例
    collector = StockDataCollector()
    
    # 获取股票列表
    stock_list = collector.fetch_stock_list()
    
    # 打印数据基本信息
    print("\n=== 股票列表数据概览 ===")
    print(f"总共获取到 {len(stock_list)} 只股票")
    print("\n前5只股票信息：")
    print(stock_list.head())
    
    # 打印一些统计信息
    print("\n=== 交易状态分布 ===")
    status_stats = stock_list['status'].value_counts()
    print(status_stats)
    
    # 保存数据到CSV文件（方便查看完整数据）
    stock_list.to_csv('stock_list.csv', index=False, encoding='utf-8-sig')
    print("\n数据已保存到 stock_list.csv")


def test_fetch_financial_data():
    # 创建收集器实例
    collector = StockDataCollector()
    
    # 测试获取浦发银行(sh.600000)的财务数据
    stock_code = "sh.600000"
    year = 2023
    quarter = 3  # 测试2023年第3季度的数据
    
    print(f"\n=== 获取 {stock_code} 的财务数据 ({year}年第{quarter}季度) ===")
    financial_data = collector.fetch_financial_data(stock_code, year, quarter)
    
    # 创建输出目录
    output_dir = f"financial_data_{stock_code.replace('.', '_')}_{year}Q{quarter}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存并显示各个报表的数据
    for report_name, df in financial_data.items():
        if not df.empty:
            # 保存到CSV
            output_file = f"{output_dir}/{report_name}.csv"
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
            # 打印预览
            print(f"\n{report_name.upper()} 报表预览：")
            print(f"字段列表：{df.columns.tolist()}")
            print(f"数据行数：{len(df)}")
            print("\n前几行数据：")
            print(df.head())
            print(f"\n完整数据已保存到：{output_file}")


if __name__ == "__main__":
    # test_fetch_stock_list()
    test_fetch_financial_data() 