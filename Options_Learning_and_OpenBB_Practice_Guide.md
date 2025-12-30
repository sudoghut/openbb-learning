# Options Learning and OpenBB Practice Guide

> A systematic learning path designed for beginners with no financial background

---

## ⚠️ OpenBB Usage Notes

### 1. Correct Way to Get Expiration Dates

```python
# ❌ May cause errors
expirations = obb.derivatives.options.expirations("SPY")

# ✅ Correct method: Extract from option chain
chains = obb.derivatives.options.chains("SPY")
expirations = sorted(chains['expiration'].unique())
```

### 2. Filter Valid Greeks Data

Some expiration dates have no Greeks data (all zeros), must filter:

```python
# Filter options with Greeks data
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]
```

---

## Phase 1: Financial Fundamentals

### 1.1 What is a Stock

A stock represents ownership shares in a company. When you buy one share of Apple (AAPL), you own a small part of Apple Inc.

**Core Concepts:**
- **Market Price**: The current price to buy or sell a stock
- **Volume**: The number of shares traded during a period
- **Market Cap**: Total company value = Stock Price × Total Shares

**OpenBB Practice:**
```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

# Get Apple's basic quote
quote = obb.equity.price.quote("AAPL")
print(quote)

# Get historical price data
history = obb.equity.price.historical(symbol="AAPL", start_date="2024-01-01")
print(history.head())
```

### 1.2 What are Derivatives

Derivatives are financial contracts whose value is "derived" from other assets (called "underlying assets").

**Main Types:**
- **Options**: Give you the right (but not obligation) to buy or sell an asset at a specific price
- **Futures**: Obligation to buy or sell an asset at a specific price on a future date
- **Swaps**: Contracts to exchange cash flows

---

## Phase 2: Options Core Concepts

### 2.1 Options Basics

**Two Types of Options:**

| Type | Right | Outlook |
|------|-------|---------|
| Call | Buy the underlying asset at the strike price | Bullish |
| Put | Sell the underlying asset at the strike price | Bearish |

**Key Terms:**
- **Strike Price**: The price specified in the option contract for buying/selling
- **Expiration Date**: The date when the option expires
- **DTE (Days to Expiration)**: Days until expiration
- **Premium**: The cost to purchase an option
- **Underlying Asset**: The stock or other asset the option is based on

### 2.2 Option Value Components

Option Value = **Intrinsic Value** + **Time Value**

**Intrinsic Value:**
- Call Option: Max(Stock Price - Strike Price, 0)
- Put Option: Max(Strike Price - Stock Price, 0)

**Time Value:**
- The "hope" that the option might become profitable before expiration
- Decays gradually as expiration approaches

### 2.3 Option Status

| Status | Call Option | Put Option |
|--------|-------------|------------|
| In-the-Money (ITM) | Stock Price > Strike | Stock Price < Strike |
| At-the-Money (ATM) | Stock Price ≈ Strike | Stock Price ≈ Strike |
| Out-of-the-Money (OTM) | Stock Price < Strike | Stock Price > Strike |

**OpenBB Practice - Get Option Chain:**
```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

# Get option chain
chains = obb.derivatives.options.chains("SPY")
current_price = chains['underlying_price'].iloc[0]
print(f"Stock Price: ${current_price}, Option Count: {len(chains)}")

# Get all expiration dates
expirations = sorted(chains['expiration'].unique())
print(f"Expirations: {expirations[:5]}")
```

---

## Phase 3: The Greeks

Greeks are measures of option price sensitivity to various factors - they are the core of options trading.

### ⚠️ Important: How to Get Meaningful Greeks Data

**Problem: Why are my Deltas all 0 or 1?**

This is because you're looking at:
1. **Expired options** (dte <= 0)
2. **Some expiration dates have no Greeks data**
3. **Deep ITM/OTM options** (too far from current stock price)

**Solution:**

```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

chains = obb.derivatives.options.chains("AAPL")
current_price = chains['underlying_price'].iloc[0]

# Key filter: dte >= 7 and delta != 0
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]

# Select an expiration date
expiry = sorted(valid['expiration'].unique())[0]
selected = valid[valid['expiration'] == expiry]

# Filter ATM Call options (±5%)
calls = selected[selected['option_type'] == 'call']
atm = calls[(calls['strike'] >= current_price * 0.95) & (calls['strike'] <= current_price * 1.05)]

print(f"Stock Price: ${current_price:.2f}, Expiration: {expiry}")
print(atm[['strike', 'delta', 'gamma', 'theta', 'vega']].to_string(index=False))
```

### 3.1 Delta (Δ) - Directional Sensitivity

**Definition:** The change in option price when the underlying moves $1

**Value Range:**
- Call Options: 0 to +1
- Put Options: -1 to 0
- ATM Options: approximately ±0.5

**Practical Meaning:**
- Delta = 0.5 → If stock rises $1, option rises $0.50
- Can also be interpreted as the probability of expiring ITM

**Typical Value Reference:**

| Option Status | Delta (Call) | Delta (Put) |
|---------------|--------------|-------------|
| Deep ITM | 0.9 - 1.0 | -0.9 to -1.0 |
| ATM | ~0.5 | ~-0.5 |
| Deep OTM | 0.0 - 0.1 | -0.1 to 0.0 |

**Example:**
```
SPY current price $500
Call Strike $500, Delta = 0.50
If SPY rises to $501:
Option price expected to rise ~$0.50
```

### 3.2 Gamma (Γ) - Rate of Delta Change

**Definition:** The change in Delta when the underlying moves $1

**Characteristics:**
- ATM options have the highest Gamma
- Deep ITM/OTM options have Gamma near 0
- Near expiration, ATM option Gamma increases dramatically

**Why It Matters:**
- Measures how frequently Delta hedging needs adjustment
- Higher Gamma = faster Delta changes = higher risk

### 3.3 Theta (Θ) - Time Decay

**Definition:** The amount of value lost per day (usually negative)

**Characteristics:**
- Option buyers "lose" time value every day
- Theta decay accelerates near expiration
- OTM options decay fastest before expiration

**Analogy:** Like holding an ice cream cone - it melts with every passing second

### 3.4 Vega (ν) - Volatility Sensitivity

**Definition:** The change in option price when implied volatility changes 1%

**Characteristics:**
- All options have positive Vega
- ATM options have the highest Vega
- Longer time to expiration = higher Vega

**Implied Volatility (IV):**
- Market's expectation of future volatility
- Cannot be directly observed; derived from option prices
- IV rises → Option prices rise

### 3.5 Greeks Quick Reference

| Greek | Measures | Call | Put | Max at ATM? |
|-------|----------|------|-----|-------------|
| Delta | Stock price sensitivity | 0 to +1 | -1 to 0 | - |
| Gamma | Delta change rate | Positive | Positive | ✓ |
| Theta | Time decay | Negative | Negative | ✓ |
| Vega | Volatility sensitivity | Positive | Positive | ✓ |

---

## Phase 4: OpenBB Data Analysis Practice (Ongoing)

### 4.1 Options Analysis Workflow

```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

symbol = "AAPL"
chains = obb.derivatives.options.chains(symbol)
current_price = chains['underlying_price'].iloc[0]

# Filter valid options
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]

# Select an expiration date
expiry = sorted(valid['expiration'].unique())[0]
selected = valid[valid['expiration'] == expiry]

# Analyze near ATM
calls = selected[selected['option_type'] == 'call']
puts = selected[selected['option_type'] == 'put']

atm_calls = calls[(calls['strike'] >= current_price * 0.95) & (calls['strike'] <= current_price * 1.05)]
atm_puts = puts[(puts['strike'] >= current_price * 0.95) & (puts['strike'] <= current_price * 1.05)]

print(f"Stock Price: ${current_price:.2f}, Expiration: {expiry}")
print("\nCall Options:")
print(atm_calls[['strike', 'delta', 'gamma', 'theta', 'vega', 'bid', 'ask']].to_string(index=False))
print("\nPut Options:")
print(atm_puts[['strike', 'delta', 'gamma', 'theta', 'vega', 'bid', 'ask']].to_string(index=False))
```

### 4.2 Visualizing Greeks

```python
from openbb import obb
import matplotlib.pyplot as plt

obb.user.preferences.output_type = "dataframe"

chains = obb.derivatives.options.chains("SPY")
current_price = chains['underlying_price'].iloc[0]

# Filter valid options
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]

# Select Calls for one expiration
expiry = sorted(valid['expiration'].unique())[0]
calls = valid[(valid['expiration'] == expiry) & (valid['option_type'] == 'call')]
calls = calls[(calls['strike'] >= current_price * 0.85) & (calls['strike'] <= current_price * 1.15)]
calls = calls.sort_values('strike')

# Plot
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
```

### 4.3 Implied Volatility Smile Analysis

```python
from openbb import obb
import matplotlib.pyplot as plt

obb.user.preferences.output_type = "dataframe"

chains = obb.derivatives.options.chains("SPY")
current_price = chains['underlying_price'].iloc[0]

# Filter valid options with IV
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['implied_volatility'] > 0)]

# Select an expiration date
expiry = sorted(valid['expiration'].unique())[0]
selected = valid[valid['expiration'] == expiry]
selected = selected[(selected['strike'] >= current_price * 0.85) & (selected['strike'] <= current_price * 1.15)]

calls = selected[selected['option_type'] == 'call'].sort_values('strike')
puts = selected[selected['option_type'] == 'put'].sort_values('strike')

# Plot
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
```

**Understanding the Volatility Smile:**

The "Volatility Smile" phenomenon:

1. In theory, options with the same expiration should have the same IV
2. In practice, deep OTM options often have higher IV, forming a "smile" shape
3. Stock options commonly show "Volatility Skew": lower strike Puts have higher IV, reflecting market concern about "black swan" downside events
4. Trading implication: High IV options are relatively "expensive", low IV options are relatively "cheap"

---

## Phase 5: Advanced Learning Projects

### Project 1: Options Screener

```python
from openbb import obb
import pandas as pd

obb.user.preferences.output_type = "dataframe"

def screen_high_iv(symbols, min_iv=0.5):
    """Screen for high implied volatility options"""
    results = []
    for symbol in symbols:
        try:
            chains = obb.derivatives.options.chains(symbol)
            high_iv = chains[(chains['dte'] >= 14) & (chains['implied_volatility'] > min_iv)]
            if len(high_iv) > 0:
                results.append({
                    'symbol': symbol,
                    'count': len(high_iv),
                    'max_iv': high_iv['implied_volatility'].max(),
                    'avg_iv': high_iv['implied_volatility'].mean()
                })
        except:
            pass
    return pd.DataFrame(results).sort_values('max_iv', ascending=False)

symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA']
print(screen_high_iv(symbols))
```

### Project 2: Option Strategy Payoff Chart

```python
import numpy as np
import matplotlib.pyplot as plt

def plot_payoff(strike, premium, option_type='call', position='long'):
    """Plot option payoff at expiration"""
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

# Example
plot_payoff(strike=100, premium=5, option_type='call', position='long')
```

**Understanding Payoff Charts:**

Assumptions: Strike = $100, Premium = $5

- **Long Call**: Max loss $5, max profit unlimited, breakeven at $105
- **Long Put**: Max loss $5, max profit $95, breakeven at $95
- **Short Call**: Max profit $5, max loss unlimited, extremely risky
- **Short Put**: Max profit $5, max loss $95

---

## Recommended Learning Resources

### Free Resources

1. **OpenBB Official Documentation**
   - Options functions: https://docs.openbb.co/platform/reference/derivatives/options
   - Python interface: https://docs.openbb.co/python

2. **Options Basics**
   - Investopedia Options Guide
   - Khan Academy Finance Courses
   - CBOE Educational Resources

3. **Python for Finance**
   - PyQuant News: https://pyquantnews.com
   - AlgoTrading101 Blog

### Recommended Books

1. **"Options, Futures, and Other Derivatives"** - John Hull (Classic options textbook)
2. **"Option Volatility and Pricing"** - Sheldon Natenberg
3. **"Python for Finance"** - Yves Hilpisch

---

## FAQ - Frequently Asked Questions

### Q1: Why are my Greeks all 0 or 1?

**Reason:** Some expiration dates don't include Greeks data.

**Solution:** Add `delta != 0` when filtering:
```python
valid = chains[(chains['dte'] >= 7) & (chains['delta'] != 0)]
```

### Q2: What if `obb.derivatives.options.expirations()` throws an error?

**Solution:** Extract expiration dates directly from the option chain:
```python
chains = obb.derivatives.options.chains("SPY")
expirations = sorted(chains['expiration'].unique())
```

### Q3: Why is implied volatility (IV) showing 0?

**Possible Reason:** The option has no trading volume, making IV calculation impossible.

**Solution:** Filter for options with IV:
```python
valid = chains[chains['implied_volatility'] > 0]
```

### Q4: Is OpenBB data real-time?

The default CBOE data has 15-20 minute delay. For real-time data, you need to configure a paid API (e.g., Tradier, Intrinio).

### Q5: How do I get more data sources?

1. Visit https://my.openbb.co to register an account
2. Add your API keys
3. Specify the provider in your code:
```python
chains = obb.derivatives.options.chains("SPY", provider="tradier")
```

---

## Learning Checklist

### Foundation Phase
- [ ] Understand basic stock concepts
- [ ] Can use OpenBB to get stock quotes and historical data
- [ ] Understand what derivatives are

### Options Concepts
- [ ] Understand the difference between Calls and Puts
- [ ] Understand strike price, expiration date, premium
- [ ] Can distinguish ITM, ATM, OTM options
- [ ] Can use OpenBB to get and filter valid option chains

### Greeks
- [ ] Understand Delta's meaning and application
- [ ] Understand the relationship between Gamma and Delta
- [ ] Understand Theta time decay
- [ ] Understand the relationship between Vega and volatility
- [ ] Can observe correct Greeks curves

### Advanced
- [ ] Can plot Greeks charts
- [ ] Can analyze implied volatility smile
- [ ] Can plot option strategy payoff charts
- [ ] Try building an options screener

---

*Good luck with your learning! Feel free to ask questions.*
