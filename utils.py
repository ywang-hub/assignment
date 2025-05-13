# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from scipy.stats import zscore

def get_bond_yield():
    """无风险利率（强制设为0）"""
    return pd.Series([0.00], index=[datetime.now().date()])

def get_hs300_symbols():
    """获取沪深300成分股"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            components = ak.index_stock_cons_csindex(symbol="000300")
            symbols = components['成分券代码'].unique().tolist()
            return [f"{s}.{'SH' if s.startswith('6') else 'SZ'}" for s in symbols]
        except:
            components = ak.index_stock_cons_sina(symbol="hs300")
            symbols = components['code'].unique().tolist()
            return [f"{s}.{'SH' if s.startswith('6') else 'SZ'}" for s in symbols]

def get_stock_data(symbol, retries=3):
    """获取单只股票数据"""
    for attempt in range(retries):
        try:
            df = ak.stock_zh_a_hist(
                symbol=symbol.replace('.SH', '').replace('.SZ', ''),
                period="daily",
                start_date="20210101",
                end_date="20250430",
                adjust="hfq"
            )
            df['symbol'] = symbol
            return df.set_index('日期')
        except:
            time.sleep(1)
    return pd.DataFrame()

def cross_section_normalize(factors):
    """横截面标准化"""
    return factors.apply(lambda s: zscore(s, nan_policy='omit'), axis=1).ffill().fillna(0)

def align_factors(*factor_dfs):
    """数据对齐"""
    common_index = factor_dfs[0].index
    for df in factor_dfs[1:]:
        common_index = common_index.intersection(df.index)
    return [df.loc[common_index] for df in factor_dfs]
