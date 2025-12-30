from openbb import obb
import pandas as pd

obb.user.preferences.output_type = "dataframe"

def screen_high_iv(symbols, min_iv=0.5):
    """筛选高隐含波动率的期权"""
    results = []
    for symbol in symbols:
        try:
            chains = obb.derivatives.options.chains(symbol)
            high_iv = chains[(chains['dte'] >= 14) & (chains['implied_volatility'] > min_iv)]
            if len(high_iv) > 0:
                results.append({
                    'symbol': symbol,
                    'count': len(high_iv),
                    'max_iv': high_iv['implied_volatility'].max()
                })
        except:
            pass
    return pd.DataFrame(results).sort_values('max_iv', ascending=False)

symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA']
print(screen_high_iv(symbols))