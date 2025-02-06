"""
主程序入口
整合所有模块，提供完整的程序功能
"""

from stock_data_collector import StockDataCollector
from stock_screener import StockScreener
from stock_viewer import StockViewer


def main():
    # 初始化各个模块
    collector = StockDataCollector()
    screener = StockScreener()
    viewer = StockViewer()
    
    # TODO: 实现主程序逻辑
    
    
if __name__ == "__main__":
    main() 