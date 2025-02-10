"""测试股票筛选功能"""
import pandas as pd
from stock_screener import StockScreener

def load_financial_data(year, quarter):
    try:
        balance_data = pd.read_csv(f'financial_data_all_{year}Q{quarter}_cn/balance_all.csv')
        return balance_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def main():
    # 创建股票筛选器
    screener = StockScreener()
    
    # 添加资产负债筛选条件
    screener.add_filter('balance', 'liabilityToAsset(资产负债率)', max_value=0.008)
    screener.add_filter('balance', 'quickRatio(速动比率)', min_value=1.0, allow_null=True)  # 速动比率大于1.0
    screener.add_filter('balance', 'YOYLiability(负债同比增长率)', min_value=0, allow_null=True)  # 负债同比增长率大于0，表示负债在增长，需要注意资产规模是否同步增长
    
    # 加载2024年第三季度数据
    data = load_financial_data(2024, 3)
    if data is not None:
        # 执行筛选
        results = screener.screen(data)
        print(f"找到 {len(results)} 只符合条件的股票")
        
        if len(results) > 0:
            # 显示前10只股票
            print("\n前10只股票：")
            for _, row in results.head(10).iterrows():
                print(f"{row['code(股票代码)']} - {row['stock_name(股票名称)']}")
            
            # 保存结果
            results.to_csv('screener_results.csv', index=False)
            print("\n完整结果已保存到 screener_results.csv")

if __name__ == "__main__":
    main() 