import pandas as pd
import numpy as np

def calculate_realized_volatility(close):
    """波动率因子"""
    factors = pd.DataFrame(index=close.index, columns=close.columns)
    market_vol = close.pct_change().std(axis=1).rolling(60).mean()
    
    for stock in close.columns:
        log_ret = np.log(close[stock]/close[stock].shift(1))
        
        vol_10d = log_ret.rolling(10).std()
        vol_20d = log_ret.rolling(20).std()
        vol_60d = log_ret.rolling(60).std()
        
        # 综合计算
        factors[stock] = -(
            vol_20d.rank() * 0.4 +
            (vol_10d/vol_20d).rank() * 0.2 +
            (vol_20d/vol_60d).rank() * 0.2 +
            (vol_20d > vol_60d).rolling(5).sum().rank() * 0.1 +
            (vol_20d / market_vol).rank() * 0.1
        )
    
    return factors
