import numpy as np
import matplotlib.pyplot as plt

def plot_payoff(strike, premium, option_type='call', position='long'):
    """绘制期权到期收益图"""
    prices = np.linspace(strike * 0.7, strike * 1.3, 100)
    
    if option_type == 'call':
        payoff = np.maximum(prices - strike, 0) - premium
    else:
        payoff = np.maximum(strike - prices, 0) - premium
    
    if position == 'short':
        payoff = -payoff
    
    plt.figure(figsize=(10, 6))
    plt.plot(prices, payoff, 'b-', linewidth=2)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.axvline(x=strike, color='red', linestyle='--', label=f'Strike ${strike}')
    plt.fill_between(prices, payoff, 0, where=(payoff > 0), alpha=0.3, color='green')
    plt.fill_between(prices, payoff, 0, where=(payoff < 0), alpha=0.3, color='red')
    plt.xlabel('Stock Price at Expiration')
    plt.ylabel('Profit/Loss')
    plt.title(f'{position.upper()} {option_type.upper()} | Strike=${strike}, Premium=${premium}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# 示例
plot_payoff(strike=100, premium=5, option_type='call', position='long')