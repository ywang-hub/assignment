# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils import *
from factors.quality_factor import calculate_quality_factors
from factors.volatility_factor import calculate_realized_volatility
from factors.liquidity_factor import calculate_liquidity_factor
from factors.rsi_factor import calculate_rsi

def main():
    # 数据获取
    symbols = get_hs300_symbols()
    dfs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(get_stock_data, sym): sym for sym in symbols}
        for future in as_completed(futures):
            dfs.append(future.result())
    
    # 数据预处理
    full_data = pd.concat(dfs)
    close = full_data.pivot_table(index='日期', columns='symbol', values='收盘').ffill()
    volume = full_data.pivot_table(index='日期', columns='symbol', values='成交量')[close.columns]

    # 计算因子
    quality = cross_section_normalize(calculate_quality_factors(close, volume))
    volatility = cross_section_normalize(calculate_realized_volatility(close))
    liquidity = cross_section_normalize(calculate_liquidity_factor(close, volume))
    rsi = cross_section_normalize(calculate_rsi(close))

    # 对齐因子
    factors = align_factors(quality, volatility, liquidity, rsi)
    factor_names = ['Quality', 'Volatility', 'Liquidity', 'RSI']
    factor_df = pd.concat([f.mean(axis=1) for f in factors], axis=1)
    factor_df.columns = factor_names

    # 计算相关系数
    corr_matrix = factor_df.corr()
    sns.heatmap(corr_matrix, annot=True)
    plt.title("Factor Correlation Matrix")
    plt.savefig('correlation_matrix.png')

if __name__ == "__main__":
    main()
