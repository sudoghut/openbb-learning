from openbb import obb

obb.user.preferences.output_type = "dataframe"

# 获取带 Greeks 的期权链
chains = obb.derivatives.options.chains(symbol="AAPL", provider="cboe")

# 筛选特定到期日的 Call 期权
calls = chains[chains['option_type'] == 'call']

# 查看 Greeks 列
greek_columns = ['strike', 'delta', 'gamma', 'theta', 'vega', 'implied_volatility']
print(calls[greek_columns].head(20))