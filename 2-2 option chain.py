from openbb import obb

obb.user.preferences.output_type = "dataframe"

symbol = "SPY"

# 获取期权链
chains = obb.derivatives.options.chains(symbol=symbol)

# 从期权链中提取所有到期日（替代 expirations 方法）
expirations = sorted(chains['expiration'].unique())
print(f"可用的到期日 (前10个):")
for exp in expirations[:10]:
    print(f"  {exp}")

# 查看期权链基本信息
print(f"\n期权链共有 {len(chains)} 个合约")
print(f"列名: {list(chains.columns)}")