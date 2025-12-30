def analyze_volatility_smile(symbol="SPY", min_dte=14):
    """
    分析波动率微笑
    """
    from openbb import obb
    import matplotlib.pyplot as plt
    
    obb.user.preferences.output_type = "dataframe"
    
    chains = obb.derivatives.options.chains(symbol=symbol)
    current_price = chains['underlying_price'].iloc[0]
    
    # 筛选有效期权
    valid = chains[(chains['dte'] >= min_dte) & (chains['implied_volatility'] > 0)]
    if len(valid) == 0:
        print("没有有效数据")
        return
    
    target_expiry = sorted(valid['expiration'].unique())[0]
    selected = valid[valid['expiration'] == target_expiry]
    
    # 筛选合理范围
    selected = selected[
        (selected['strike'] >= current_price * 0.85) & 
        (selected['strike'] <= current_price * 1.15)
    ]
    
    calls = selected[selected['option_type'] == 'call'].sort_values('strike')
    puts = selected[selected['option_type'] == 'put'].sort_values('strike')
    
    # 绘图
    plt.figure(figsize=(10, 6))
    
    if len(calls) > 0:
        plt.plot(calls['strike'], calls['implied_volatility'] * 100, 
                 'b-o', label='Call IV', markersize=4)
    
    if len(puts) > 0:
        plt.plot(puts['strike'], puts['implied_volatility'] * 100, 
                 'r--s', label='Put IV', markersize=4)
    
    plt.axvline(x=current_price, color='green', linestyle=':', 
                linewidth=2, label=f'当前股价 ${current_price:.2f}')
    
    plt.xlabel('执行价 (Strike)')
    plt.ylabel('隐含波动率 (%)')
    plt.title(f'{symbol} 波动率微笑 (到期日: {target_expiry})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('volatility_smile.png', dpi=150, bbox_inches='tight')
    print("图表已保存为 'volatility_smile.png'")
    plt.show()

# 使用
analyze_volatility_smile("SPY", min_dte=14)