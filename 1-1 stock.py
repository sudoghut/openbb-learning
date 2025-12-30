from openbb import obb

# 获取苹果公司的基本报价
quote = obb.equity.price.quote("AAPL")
print(quote.to_dataframe())

# 获取历史价格数据
history = obb.equity.price.historical(
    symbol="AAPL", 
    start_date="2024-01-01"
)
print(history.to_dataframe())