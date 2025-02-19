"""测试股票筛选功能"""
import pandas as pd
from stock_screener import StockScreener

def load_financial_data(year, quarter):
    try:
        # 加载各类财务数据
        balance_data = pd.read_csv(f'financial_data_all_{year}Q{quarter}_cn/balance_all.csv')
        profit_data = pd.read_csv(f'financial_data_all_{year}Q{quarter}_cn/profit_all.csv')
        indicators_data = pd.read_csv(f'financial_data_all_{year}Q{quarter}_cn/indicators_all.csv')
        
        # 加载上一年同期数据用于计算同比增长
        try:
            last_year_profit = pd.read_csv(f'financial_data_all_{year-1}Q{quarter}_cn/profit_all.csv')
            # 计算净利润同比增长率
            profit_data = profit_data.merge(
                last_year_profit[['code(股票代码)', 'netProfit(净利润)']],
                on='code(股票代码)',
                how='left',
                suffixes=('', '_last_year')
            )
            # 计算增长率
            profit_data['netProfit_growth'] = (profit_data['netProfit(净利润)'] - profit_data['netProfit(净利润)_last_year']) / abs(profit_data['netProfit(净利润)_last_year'])
            
            # 计算净利润规模（以亿为单位）
            profit_data['netProfit_scale'] = profit_data['netProfit(净利润)'] / 100000000
            
        except Exception as e:
            print(f"无法加载上年同期数据，跳过增长率计算: {e}")
            profit_data['netProfit_growth'] = None
            profit_data['netProfit_scale'] = None
        
        # 合并数据
        merged_data = balance_data.merge(profit_data, on=['code(股票代码)', 'stock_name(股票名称)'], how='left')
        merged_data = merged_data.merge(indicators_data, on=['code(股票代码)', 'stock_name(股票名称)'], how='left')
        
        return merged_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def main():
    # 创建股票筛选器
    screener = StockScreener()
    
    # 1. 偿债能力指标（保持严格的资产负债率要求）
    screener.add_filter('balance', 'liabilityToAsset(资产负债率)', max_value=0.006)  # 资产负债率  <0.6%
    
    # 2. 盈利能力指标
    screener.add_filter('profit', 'roeAvg(平均净资产收益率)', min_value=0.15, allow_null=False)  # ROE>15%
    screener.add_filter('profit', 'npMargin(净利率)', min_value=0.15, allow_null=False)  # 净利率>15%
    screener.add_filter('profit', 'netProfit_growth', min_value=0.001, allow_null=False)  # 净利润同比增长>0.1%
    
    # 3. 运营效率指标
    # screener.add_filter('indicators', 'dupontAssetTurn(总资产周转率)', min_value=0.8, allow_null=False)  # 提高总资产周转率要求
    
    # 4. 现金流指标
    screener.add_filter('indicators', 'dupontNitogr(净利润/营业总收入)', min_value=0.05, allow_null=False)  # 提高利润率要求
    
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