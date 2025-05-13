import pandas as pd

def calculate_quality_factors(close, volume):
    """质量因子计算"""
    factors = pd.DataFrame(index=close.index, columns=close.columns)
    
    for stock in close.columns:
        # 动量计算
        mom_3m = close[stock].pct_change(63)
        mom_6m = (close[stock].shift(21) / close[stock].shift(126) - 1)
        
        # 成交量稳定性
        vol_std = volume[stock].pct_change().rolling(60).std()
        
        # 综合评分
        factors[stock] = (
            mom_3m.rank() * 0.4 + 
            mom_6m.rank() * 0.4 + 
            (-vol_std).rank() * 0.2
        )
    
    return factors
