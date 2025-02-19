"""测试获取股票估值数据"""
from stock_data_collector import StockDataCollector
import pandas as pd

def test_stock_valuation():
    # 创建收集器实例
    collector = StockDataCollector()
    
    # 测试股票列表
    test_stocks = [
        "sh.603871",  # 嘉友国际
        "sh.688506",  # 百利天恒
        "sz.300641",  # 正丹股份
        "sz.300979",  # 华利集团
        "sz.301004",  # 嘉益股份
        "sz.301617"   # 博苑股份
    ]
    
    print(f"\n=== 获取 {len(test_stocks)} 只股票的估值数据 ===")
    
    # 获取每只股票的估值数据
    valuation_data = []
    for stock_code in test_stocks:
        # 获取基本面数据
        rs = collector.bs.query_stock_basic(code=stock_code)
        if rs.error_code != '0':
            print(f'获取{stock_code}基本信息失败: {rs.error_msg}')
            continue
            
        # 获取当日行情数据
        rs_k = collector.bs.query_history_k_data_plus(
            code=stock_code,
            fields="date,code,close,volume,amount,turn,peTTM,pbMRQ,psTTM",
            start_date='2024-01-01',
            end_date='2024-01-31',
            frequency="d",
            adjustflag="3"
        )
        
        if rs.error_code == '0' and rs_k.error_code == '0':
            # 获取最新的行情数据
            latest_data = None
            while rs_k.next():
                latest_data = rs_k.get_row_data()
            
            if latest_data:
                valuation_data.append({
                    'code': stock_code,
                    'price': float(latest_data[2]) if latest_data[2] != '' else None,
                    'volume': float(latest_data[3]) if latest_data[3] != '' else None,
                    'amount': float(latest_data[4]) if latest_data[4] != '' else None,
                    'turnover': float(latest_data[5]) if latest_data[5] != '' else None,
                    'pe_ttm': float(latest_data[6]) if latest_data[6] != '' else None,
                    'pb': float(latest_data[7]) if latest_data[7] != '' else None,
                    'ps': float(latest_data[8]) if latest_data[8] != '' else None
                })
    
    # 转换为DataFrame并显示结果
    if valuation_data:
        df = pd.DataFrame(valuation_data)
        print("\n估值数据概览：")
        print(df.to_string(index=False))
        
        # 计算平均值
        print("\n平均估值指标：")
        mean_values = df[['pe_ttm', 'pb', 'ps']].mean()
        print(f"平均市盈率(TTM): {mean_values['pe_ttm']:.2f}")
        print(f"平均市净率: {mean_values['pb']:.2f}")
        print(f"平均市销率: {mean_values['ps']:.2f}")
        
        # 保存结果
        df.to_csv('valuation_results.csv', index=False, encoding='utf-8-sig')
        print("\n数据已保存到 valuation_results.csv")
    else:
        print("未获取到估值数据")

if __name__ == "__main__":
    test_stock_valuation() 