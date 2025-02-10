"""
为财务数据添加中文指标名称
"""

import pandas as pd
import os
import glob

# 定义各个报表指标的中文名称映射
INDICATOR_NAMES = {
    # 利润表指标
    'roeAvg': '平均净资产收益率',
    'npMargin': '净利率',
    'gpMargin': '毛利率',
    'netProfit': '净利润',
    'epsTTM': '每股收益(TTM)',
    'MBRevenue': '主营业务收入',
    'totalShare': '总股本',
    'liqaShare': '流通股本',
    
    # 资产负债表指标
    'currentRatio': '流动比率',
    'quickRatio': '速动比率',
    'cashRatio': '现金比率',
    'YOYLiability': '负债同比增长率',
    'liabilityToAsset': '资产负债率',
    'assetToEquity': '权益乘数',
    
    # 现金流量表指标
    'CAToAsset': '流动资产/总资产',
    'NCAToAsset': '非流动资产/总资产',
    'tangibleAssetToAsset': '有形资产/总资产',
    'ebitToInterest': '已获利息倍数(EBIT/利息费用)',
    'CFOToOR': '经营活动产生的现金流量净额/营业收入',
    'CFOToNP': '经营活动产生的现金流量净额/净利润',
    'CFOToGr': '经营活动产生的现金流量净额/营业总收入',
    
    # 财务指标
    'dupontROE': '净资产收益率',
    'dupontAssetStoEquity': '权益乘数',
    'dupontAssetTurn': '总资产周转率',
    'dupontPnitoni': '净利润/营业总收入',
    'dupontNitogr': '净利润/营业总收入',
    'dupontTaxBurden': '税负比率',
    'dupontIntburden': '利息负担',
    'dupontEbittogr': 'EBIT/营业总收入',
    
    # 通用字段
    'code': '股票代码',
    'pubDate': '发布日期',
    'statDate': '统计截止日',
    'stock_name': '股票名称'
}

def add_chinese_names(year, quarter):
    """为指定年份和季度的财务数据添加中文指标名称"""
    
    input_dir = f"financial_data_all_{year}Q{quarter}"
    output_dir = f"financial_data_all_{year}Q{quarter}_cn"
    
    if not os.path.exists(input_dir):
        print(f"目录不存在: {input_dir}")
        return
        
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理每个报表文件
    report_files = ['profit_all.csv', 'balance_all.csv', 'cash_flow_all.csv', 'indicators_all.csv']
    
    for file in report_files:
        input_file = os.path.join(input_dir, file)
        if not os.path.exists(input_file):
            print(f"文件不存在: {input_file}")
            continue
            
        print(f"\n处理文件: {input_dir}/{file}")
        
        # 读取CSV文件
        df = pd.read_csv(input_file)
        
        # 创建新的列名映射
        new_columns = {}
        for col in df.columns:
            if col in INDICATOR_NAMES:
                # 使用格式：英文名(中文名)
                new_columns[col] = f"{col}({INDICATOR_NAMES[col]})"
            else:
                new_columns[col] = col
        
        # 重命名列
        df = df.rename(columns=new_columns)
        
        # 保存结果
        output_file = os.path.join(output_dir, file)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"已保存处理后的文件: {output_file}")
        print(f"包含的指标：")
        for col in df.columns:
            print(f"  - {col}")

def process_all_data():
    """处理所有已下载的财务数据"""
    # 查找所有财务数据目录
    data_dirs = glob.glob("financial_data_all_*")
    data_dirs = [d for d in data_dirs if not d.endswith('_cn')]  # 排除已处理的目录
    
    if not data_dirs:
        print("未找到任何财务数据目录")
        return
        
    print(f"找到以下数据目录：")
    for dir in data_dirs:
        print(f"  - {dir}")
    
    # 处理每个目录
    for dir in data_dirs:
        # 从目录名提取年份和季度
        try:
            year_q = dir.split('_')[-1]
            year = int(year_q[:4])
            quarter = int(year_q[5])
            print(f"\n处理 {year}年第{quarter}季度的数据...")
            add_chinese_names(year, quarter)
        except Exception as e:
            print(f"处理目录 {dir} 时出错: {str(e)}")
            continue

if __name__ == "__main__":
    # 处理所有数据
    process_all_data() 