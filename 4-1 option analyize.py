from openbb import obb
import pandas as pd

obb.user.preferences.output_type = "dataframe"

def analyze_options(symbol="AAPL", min_dte=14, max_dte=60):
    """
    完整的期权分析工作流
    
    参数:
    - symbol: 股票代码
    - min_dte: 最小到期天数
    - max_dte: 最大到期天数
    """
    print(f"=" * 50)
    print(f"分析 {symbol} 的期权")
    print(f"=" * 50)
    
    # 1. 获取期权链
    chains = obb.derivatives.options.chains(symbol=symbol)
    
    # 2. 获取当前股价
    current_price = chains['underlying_price'].iloc[0]
    print(f"\n当前股价: ${current_price:.2f}")
    
    # 3. 查看所有到期日
    all_expirations = sorted(chains['expiration'].unique())
    print(f"\n所有到期日数量: {len(all_expirations)}")
    
    # 4. 筛选合适的到期日范围
    valid_options = chains[
        (chains['dte'] >= min_dte) & 
        (chains['dte'] <= max_dte)
    ]
    
    if len(valid_options) == 0:
        print(f"没有 {min_dte}-{max_dte} 天的期权，尝试放宽条件...")
        valid_options = chains[chains['dte'] > 7]
    
    if len(valid_options) == 0:
        print("错误：没有找到有效的期权数据")
        return None
    
    # 5. 选择一个到期日
    valid_expirations = sorted(valid_options['expiration'].unique())
    target_expiry = valid_expirations[0]  # 选择最近的有效到期日
    target_dte = valid_options[valid_options['expiration'] == target_expiry]['dte'].iloc[0]
    
    print(f"\n选择的到期日: {target_expiry} (还有 {target_dte} 天)")
    
    # 6. 筛选该到期日的数据
    selected = valid_options[valid_options['expiration'] == target_expiry]
    
    # 7. 分析平值附近期权
    atm_range = 0.05  # ±5%
    lower_bound = current_price * (1 - atm_range)
    upper_bound = current_price * (1 + atm_range)
    
    # Call 期权
    calls = selected[selected['option_type'] == 'call']
    atm_calls = calls[
        (calls['strike'] >= lower_bound) & 
        (calls['strike'] <= upper_bound)
    ].sort_values('strike')
    
    # Put 期权
    puts = selected[selected['option_type'] == 'put']
    atm_puts = puts[
        (puts['strike'] >= lower_bound) & 
        (puts['strike'] <= upper_bound)
    ].sort_values('strike')
    
    print(f"\n平值附近 Call 期权 (执行价 ${lower_bound:.2f} - ${upper_bound:.2f}):")
    display_cols = ['strike', 'delta', 'gamma', 'theta', 'vega', 'implied_volatility', 'bid', 'ask']
    available_cols = [c for c in display_cols if c in atm_calls.columns]
    print(atm_calls[available_cols].to_string(index=False))
    
    print(f"\n平值附近 Put 期权:")
    print(atm_puts[available_cols].to_string(index=False))
    
    return {
        'current_price': current_price,
        'expiration': target_expiry,
        'dte': target_dte,
        'calls': atm_calls,
        'puts': atm_puts
    }

# 使用示例
result = analyze_options("AAPL", min_dte=14, max_dte=45)