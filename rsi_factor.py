def calculate_rsi(close, window=21):
    """RSI因子"""
    factors = pd.DataFrame(index=close.index, columns=close.columns)
    
    for stock in close.columns:
        delta = close[stock].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()
        
        rs = avg_gain / (avg_loss + 1e-6)
        rsi = 100 - (100 / (1 + rs))
        factors[stock] = -((rsi - 50) / 30)
    
    return factors
