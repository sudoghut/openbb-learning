# OpenBB 期权学习与实践

[English](README_EN.md) | 中文

本仓库整理了一套循序渐进的期权学习路线，并配套 OpenBB 的 Python 脚本示例，帮助你从基础概念过渡到数据分析与可视化。

## 内容概览
- 分阶段学习指南：基础概念 → 期权核心 → Greeks → 数据分析实践 → 进阶项目
- 可运行的 OpenBB 示例脚本（报价、期权链、Greeks、IV、可视化、筛选器）
- 相关图像输出示例（Greeks、IV 微笑）

## 目录结构
- [`期权学习与OpenBB实践指南_v3.md`](期权学习与OpenBB实践指南_v3.md)：完整学习笔记与代码示例（中文）
- `1-1 stock.py`：股票报价与历史价格
- `2-2 option chain.py`：期权链与到期日提取
- `2-2 option chain extra.py`：期权链筛选与 Greeks 基础
- `3-5 greeks.py`：Greeks 数据查看
- `4-1 option analyize.py`：期权分析工作流
- `4-2 greeks viz.py`：Greeks 可视化
- `4-3 IV.py`：隐含波动率微笑
- `5-1 option screener.py`：高 IV 期权筛选器
- `5-2 option strategy viz.py`：期权策略收益图
- `greeks_correct.png`、`volatility_smile.png`：示例输出图

## 环境准备
- Python 3.10+
- 安装 OpenBB（按官方文档）
- 建议使用虚拟环境

## 快速开始
```powershell
# 以获取期权链为例
python ".\2-2 option chain.py"

# Greeks 可视化
python ".\4-2 greeks viz.py"
```

> Windows 路径含空格时请使用反斜杠转义或引号。

## 学习路线（简要）
1. 基础概念：股票、衍生品
2. 期权核心：价值构成、状态、到期日与 DTE
3. Greeks：Delta/Gamma/Theta/Vega
4. 数据实践：期权链筛选、Greeks 与 IV 可视化
5. 进阶项目：Screener、收益图

## 说明
- 示例以 `AAPL`、`SPY` 为主，你可替换为其他标的。
- OpenBB 数据源与权限会影响可用字段与实时性。
