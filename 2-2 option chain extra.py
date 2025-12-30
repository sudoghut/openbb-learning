from openbb import obb

obb.user.preferences.output_type = "dataframe"

symbol = "AAPL"

# 获取期权链
chains = obb.derivatives.options.chains(symbol=symbol)

# 获取当前股价
current_price = chains['underlying_price'].iloc[0]
print(f"当前股价: ${current_price:.2f}")

# ========== 关键筛选步骤 ==========

# 1. 只选择未到期的期权 (dte > 0)
active = chains[chains['dte'] > 0]
print(f"未到期期权: {len(active)} 个")

# 2. 选择有足够时间价值的期权 (建议 dte 在 14-60 天)
mid_term = active[(active['dte'] >= 14) & (active['dte'] <= 60)]
print(f"14-60天到期的期权: {len(mid_term)} 个")

# 3. 如果没有，放宽条件
if len(mid_term) == 0:
    mid_term = active[active['dte'] >= 7]
    print(f"放宽到 7 天以上: {len(mid_term)} 个")

# 4. 选择一个到期日
if len(mid_term) > 0:
    # 获取所有可用到期日，选择中间的一个
    available_expirations = sorted(mid_term['expiration'].unique())
    target_expiry = available_expirations[len(available_expirations) // 2]
    print(f"选择的到期日: {target_expiry}")
    
    # 筛选该到期日
    selected = mid_term[mid_term['expiration'] == target_expiry]
    
    # 5. 筛选平值附近的 Call 期权 (±5%)
    calls = selected[selected['option_type'] == 'call']
    atm_calls = calls[
        (calls['strike'] >= current_price * 0.95) & 
        (calls['strike'] <= current_price * 1.05)
    ].sort_values('strike')
    
    print(f"\n平值附近的 Call 期权 (股价 ${current_price:.2f} ±5%):")
    print(atm_calls[['strike', 'dte', 'delta', 'gamma', 'theta', 'vega', 'implied_volatility']])