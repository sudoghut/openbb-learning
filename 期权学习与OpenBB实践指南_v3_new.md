# 期权学习与 OpenBB 实践指南

> 为金融零基础学习者设计的系统学习路径

---

## ⚠️ OpenBB 使用注意事项

### 1. 获取到期日的正确方法

```python
# ❌ 可能报错的方法
expirations = obb.derivatives.options.expirations("SPY")

# ✅ 正确的方法：从期权链提取
chains = obb.derivatives.options.chains("SPY")
expirations = sorted(chains['expiration'].unique())
```

### 2. 筛选有效的 Greeks 数据

某些到期日的期权没有 Greeks 数据（全是0），必须筛选：

```python
# 筛选有 Greeks 数据的期权
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]
```

---

## 第一阶段：金融基础概念（1-2 周）

### 1.1 什么是股票

股票代表公司的所有权份额。当你买入一股苹果公司（AAPL）的股票，你就拥有了苹果公司的一小部分。

**核心概念：**
- **市价（Market Price）**：当前买卖股票的价格
- **交易量（Volume）**：某段时间内交易的股票数量
- **市值（Market Cap）**：公司总价值 = 股价 × 总股数

**OpenBB 实践：**
```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

# 获取苹果公司的基本报价
quote = obb.equity.price.quote("AAPL")
print(quote)

# 获取历史价格数据
history = obb.equity.price.historical(symbol="AAPL", start_date="2024-01-01")
print(history.head())
```

### 1.2 什么是衍生品

衍生品是一种金融合约，其价值"衍生"自其他资产（称为"标的资产"）。

**主要类型：**
- **期权（Options）**：给你权利（但非义务）在特定价格买卖资产
- **期货（Futures）**：有义务在未来某日期以特定价格买卖资产
- **互换（Swaps）**：交换现金流的合约

---

## 第二阶段：期权核心概念（2-3 周）

### 2.1 期权基础

**两种期权类型：**

| 类型 | 英文 | 权利 | 看涨/看跌 |
|------|------|------|-----------|
| 看涨期权 | Call | 按约定价格**买入**标的资产 | 看涨 |
| 看跌期权 | Put | 按约定价格**卖出**标的资产 | 看跌 |

**关键术语：**
- **执行价/行权价（Strike Price）**：期权合约规定的买卖价格
- **到期日（Expiration Date）**：期权失效的日期
- **DTE（Days to Expiration）**：距离到期的天数
- **权利金/期权费（Premium）**：购买期权的成本
- **标的资产（Underlying Asset）**：期权对应的股票或其他资产

### 2.2 期权的价值组成

期权价值 = **内在价值** + **时间价值**

**内在价值（Intrinsic Value）：**
- 看涨期权：Max(股价 - 执行价, 0)
- 看跌期权：Max(执行价 - 股价, 0)

**时间价值（Time Value）：**
- 期权到期前还有可能盈利的"希望"
- 随着到期日临近而逐渐衰减

### 2.3 期权状态

| 状态 | 英文 | 看涨期权 | 看跌期权 |
|------|------|----------|----------|
| 实值 | In-the-Money (ITM) | 股价 > 执行价 | 股价 < 执行价 |
| 平值 | At-the-Money (ATM) | 股价 ≈ 执行价 | 股价 ≈ 执行价 |
| 虚值 | Out-of-the-Money (OTM) | 股价 < 执行价 | 股价 > 执行价 |

**OpenBB 实践 - 获取期权链：**
```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

# 获取期权链
chains = obb.derivatives.options.chains("SPY")
current_price = chains['underlying_price'].iloc[0]
print(f"股价: ${current_price}, 期权数量: {len(chains)}")

# 获取所有到期日
expirations = sorted(chains['expiration'].unique())
print(f"到期日: {expirations[:5]}")
```

---

## 第三阶段：希腊字母 Greeks（3-4 周）

希腊字母是衡量期权价格对各种因素敏感度的指标，是期权交易的核心。

### ⚠️ 重要：如何获取有意义的 Greeks 数据

**问题：为什么我看到的 Delta 全是 0 或 1？**

这是因为你在看：
1. **已到期的期权**（dte <= 0）
2. **某些到期日没有 Greeks 数据**
3. **深度实值/虚值期权**（离当前股价太远）

**解决方案：**

```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

chains = obb.derivatives.options.chains("AAPL")
current_price = chains['underlying_price'].iloc[0]

# 关键筛选：dte >= 7 且 delta != 0
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]

# 选择一个到期日
expiry = sorted(valid['expiration'].unique())[0]
selected = valid[valid['expiration'] == expiry]

# 筛选平值附近的 Call 期权 (±5%)
calls = selected[selected['option_type'] == 'call']
atm = calls[(calls['strike'] >= current_price * 0.95) & (calls['strike'] <= current_price * 1.05)]

print(f"股价: ${current_price:.2f}, 到期日: {expiry}")
print(atm[['strike', 'delta', 'gamma', 'theta', 'vega']].to_string(index=False))
```

### 3.1 Delta (Δ) - 方向敏感度

**定义：** 标的价格变动 1 元时，期权价格的变动量

**取值范围：**
- 看涨期权：0 到 +1
- 看跌期权：-1 到 0
- 平值期权：约 ±0.5

**实际意义：**
- Delta = 0.5 → 股价涨 1 元，期权涨 0.5 元
- 也可理解为期权到期时成为实值的概率

**典型值参考：**

| 期权状态 | Delta (Call) | Delta (Put) |
|----------|--------------|-------------|
| 深度实值 | 0.9 - 1.0 | -0.9 至 -1.0 |
| 平值 | ~0.5 | ~-0.5 |
| 深度虚值 | 0.0 - 0.1 | -0.1 至 0.0 |

**例子：**
```
SPY 现价 $500
Call 执行价 $500，Delta = 0.50
如果 SPY 涨到 $501：
期权价格预计上涨约 $0.50
```

### 3.2 Gamma (Γ) - Delta 的变化率

**定义：** 标的价格变动 1 元时，Delta 的变动量

**特点：**
- 平值期权 Gamma 最大
- 深度实值/虚值期权 Gamma 接近 0
- 临近到期时，平值期权 Gamma 急剧增加

**为什么重要：**
- 衡量 Delta 对冲需要调整的频率
- Gamma 越大，Delta 变化越快，风险越高

### 3.3 Theta (Θ) - 时间衰减

**定义：** 每过一天，期权价值的损失量（通常为负数）

**特点：**
- 期权买方每天都在"流失"时间价值
- 临近到期时，Theta 衰减加速
- 虚值期权在到期前衰减最快

**比喻：** 就像拿着冰淇淋，每过一秒都在融化

### 3.4 Vega (ν) - 波动率敏感度

**定义：** 隐含波动率变动 1% 时，期权价格的变动量

**特点：**
- 所有期权的 Vega 都是正数
- 平值期权 Vega 最大
- 到期时间越长，Vega 越大

**隐含波动率（IV）：**
- 市场对未来波动的预期
- 不能直接观察，由期权价格反推
- IV 上升 → 期权价格上升

### 3.5 Greeks 速查表

| Greek | 衡量什么 | Call | Put | 平值最大? |
|-------|----------|------|-----|-----------|
| Delta | 股价敏感度 | 0 到 +1 | -1 到 0 | - |
| Gamma | Delta 变化率 | 正 | 正 | ✓ |
| Theta | 时间衰减 | 负 | 负 | ✓ |
| Vega | 波动率敏感度 | 正 | 正 | ✓ |

---

## 第四阶段：OpenBB 数据分析实践（持续）

### 4.1 期权分析工作流

```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

symbol = "AAPL"
chains = obb.derivatives.options.chains(symbol)
current_price = chains['underlying_price'].iloc[0]

# 筛选有效期权
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]

# 选择一个到期日
expiry = sorted(valid['expiration'].unique())[0]
selected = valid[valid['expiration'] == expiry]

# 分析平值附近
calls = selected[selected['option_type'] == 'call']
puts = selected[selected['option_type'] == 'put']

atm_calls = calls[(calls['strike'] >= current_price * 0.95) & (calls['strike'] <= current_price * 1.05)]
atm_puts = puts[(puts['strike'] >= current_price * 0.95) & (puts['strike'] <= current_price * 1.05)]

print(f"股价: ${current_price:.2f}, 到期日: {expiry}")
print("\nCall 期权:")
print(atm_calls[['strike', 'delta', 'gamma', 'theta', 'vega', 'bid', 'ask']].to_string(index=False))
print("\nPut 期权:")
print(atm_puts[['strike', 'delta', 'gamma', 'theta', 'vega', 'bid', 'ask']].to_string(index=False))
```

### 4.2 可视化 Greeks

```python
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
```

### 4.3 隐含波动率微笑分析

```python
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
```

**波动率微笑解读：**

"波动率微笑" (Volatility Smile) 现象：

1. 理论上，同一到期日的期权应该有相同的 IV
2. 实际上，深度虚值期权的 IV 往往更高，形成"微笑"形状
3. 股票期权常见"波动率倾斜"(Skew)：低执行价的 Put 的 IV 更高，反映市场对"黑天鹅"下跌的担忧
4. 交易含义：IV 高的期权相对"贵"，IV 低的期权相对"便宜"

---

## 第五阶段：进阶学习项目

### 项目 1：期权 Screener

```python
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
                    'max_iv': high_iv['implied_volatility'].max(),
                    'avg_iv': high_iv['implied_volatility'].mean()
                })
        except:
            pass
    return pd.DataFrame(results).sort_values('max_iv', ascending=False)

symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA']
print(screen_high_iv(symbols))
```

### 项目 2：期权策略收益图

```python
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
```

**收益图解读：**

假设：执行价 = $100, 权利金 = $5

- **Long Call (买入看涨期权)**：最大损失 $5，最大收益无限，盈亏平衡点 $105
- **Long Put (买入看跌期权)**：最大损失 $5，最大收益 $95，盈亏平衡点 $95
- **Short Call (卖出看涨期权)**：最大收益 $5，最大损失无限，风险极高
- **Short Put (卖出看跌期权)**：最大收益 $5，最大损失 $95

---

## 学习资源推荐

### 免费资源

1. **OpenBB 官方文档**
   - 期权功能：https://docs.openbb.co/platform/reference/derivatives/options
   - Python 接口：https://docs.openbb.co/python

2. **期权基础**
   - Investopedia Options Guide
   - Khan Academy 金融课程
   - CBOE 教育资源

3. **Python 金融**
   - PyQuant News: https://pyquantnews.com
   - AlgoTrading101 博客

### 书籍推荐

1. **《Options, Futures, and Other Derivatives》** - John Hull（期权经典教材）
2. **《Option Volatility and Pricing》** - Sheldon Natenberg
3. **《Python for Finance》** - Yves Hilpisch

---

## 常见问题 FAQ

### Q1: 为什么我的 Greeks 全是 0 或 1？

**原因：** 某些到期日的期权数据不包含 Greeks。

**解决：** 筛选时加上 `delta != 0`：
```python
valid = chains[(chains['dte'] >= 7) & (chains['delta'] != 0)]
```

### Q2: `obb.derivatives.options.expirations()` 报错怎么办？

**解决：** 直接从期权链提取到期日：
```python
chains = obb.derivatives.options.chains("SPY")
expirations = sorted(chains['expiration'].unique())
```

### Q3: 为什么隐含波动率 (IV) 显示 0？

**可能原因：** 期权没有交易量，无法计算 IV。

**解决：** 筛选有 IV 的期权：
```python
valid = chains[chains['implied_volatility'] > 0]
```

### Q4: OpenBB 的数据是实时的吗？

默认的 CBOE 数据有 15-20 分钟延迟。如需实时数据，需要配置付费 API（如 Tradier、Intrinio）。

### Q5: 如何获取更多数据源？

1. 访问 https://my.openbb.co 注册账号
2. 添加你的 API 密钥
3. 在代码中指定 provider：
```python
chains = obb.derivatives.options.chains("SPY", provider="tradier")
```

---

## 学习检查清单

### 基础阶段
- [ ] 理解股票的基本概念
- [ ] 能用 OpenBB 获取股票报价和历史数据
- [ ] 理解什么是衍生品

### 期权概念
- [ ] 理解 Call 和 Put 的区别
- [ ] 理解执行价、到期日、权利金
- [ ] 能区分实值、平值、虚值期权
- [ ] 能用 OpenBB 获取并筛选有效的期权链

### Greeks
- [ ] 理解 Delta 的含义和应用
- [ ] 理解 Gamma 与 Delta 的关系
- [ ] 理解 Theta 时间衰减
- [ ] 理解 Vega 与波动率的关系
- [ ] 能观察到正确的 Greeks 曲线

### 进阶
- [ ] 能绘制期权 Greeks 图表
- [ ] 能分析隐含波动率微笑
- [ ] 能绘制期权策略收益图
- [ ] 尝试构建期权筛选工具

---

*祝你学习顺利！有问题随时问。*
