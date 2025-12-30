from openbb import obb
import matplotlib.pyplot as plt

obb.user.preferences.output_type = "dataframe"

chains = obb.derivatives.options.chains("SPY")
current_price = chains['underlying_price'].iloc[0]

# 筛选有效期权
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]

# 选择一个到期日的 Call
expiry = sorted(valid['expiration'].unique())[0]
calls = valid[(valid['expiration'] == expiry) & (valid['option_type'] == 'call')]
calls = calls[(calls['strike'] >= current_price * 0.85) & (calls['strike'] <= current_price * 1.15)]
calls = calls.sort_values('strike')

# 绘图
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].plot(calls['strike'], calls['delta'], 'b-o', markersize=3)
axes[0, 0].axvline(x=current_price, color='r', linestyle='--', label=f'Stock ${current_price:.0f}')
axes[0, 0].set_xlabel('Strike')
axes[0, 0].set_ylabel('Delta')
axes[0, 0].set_title('DELTA vs Strike')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].plot(calls['strike'], calls['gamma'], 'g-o', markersize=3)
axes[0, 1].axvline(x=current_price, color='r', linestyle='--', label=f'Stock ${current_price:.0f}')
axes[0, 1].set_xlabel('Strike')
axes[0, 1].set_ylabel('Gamma')
axes[0, 1].set_title('GAMMA vs Strike')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].plot(calls['strike'], calls['theta'], 'r-o', markersize=3)
axes[1, 0].axvline(x=current_price, color='r', linestyle='--', label=f'Stock ${current_price:.0f}')
axes[1, 0].set_xlabel('Strike')
axes[1, 0].set_ylabel('Theta')
axes[1, 0].set_title('THETA vs Strike')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(calls['strike'], calls['vega'], 'm-o', markersize=3)
axes[1, 1].axvline(x=current_price, color='r', linestyle='--', label=f'Stock ${current_price:.0f}')
axes[1, 1].set_xlabel('Strike')
axes[1, 1].set_ylabel('Vega')
axes[1, 1].set_title('VEGA vs Strike')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle(f'SPY Call Greeks | Expiry: {expiry}', fontsize=14)
plt.tight_layout()
plt.savefig('greeks_visualization.png', dpi=150)
plt.show()