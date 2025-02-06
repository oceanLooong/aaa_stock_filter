from stock_data_collector import StockDataCollector
import pandas as pd

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

if __name__ == "__main__":
    test_fetch_stock_list() 