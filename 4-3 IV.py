from openbb import obb
import matplotlib.pyplot as plt

obb.user.preferences.output_type = "dataframe"

chains = obb.derivatives.options.chains("SPY")
current_price = chains['underlying_price'].iloc[0]

# 筛选有 IV 的有效期权
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['implied_volatility'] > 0)]

# 选择一个到期日
expiry = sorted(valid['expiration'].unique())[0]
selected = valid[valid['expiration'] == expiry]
selected = selected[(selected['strike'] >= current_price * 0.85) & (selected['strike'] <= current_price * 1.15)]

calls = selected[selected['option_type'] == 'call'].sort_values('strike')
puts = selected[selected['option_type'] == 'put'].sort_values('strike')

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(calls['strike'], calls['implied_volatility'] * 100, 'b-o', label='Call IV', markersize=4)
plt.plot(puts['strike'], puts['implied_volatility'] * 100, 'r--s', label='Put IV', markersize=4)
plt.axvline(x=current_price, color='green', linestyle=':', linewidth=2, label=f'Stock ${current_price:.2f}')
plt.xlabel('Strike')
plt.ylabel('Implied Volatility (%)')
plt.title(f'SPY Volatility Smile | Expiry: {expiry}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('volatility_smile.png', dpi=150)
plt.show()