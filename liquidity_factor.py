import pandas as pd

def calculate_liquidity_factor(close, volume):
    """流动性因子"""
    factors = pd.DataFrame(index=close.index, columns=close.columns)
    
    for stock in close.columns:
        turnover = volume[stock] / volume[stock].rolling(60).mean()
        ret = close[stock].pct_change()
        money_flow = (close[stock] * volume[stock]).pct_change()
        impact = (ret / money_flow).rolling(10).mean()
        
        factors[stock] = (
            turnover.rank() * 0.6 +
            (-impact).rank() * 0.4
        )
    
    return factors
