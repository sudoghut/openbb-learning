# OpenBB Options Learning and Practice

English | [中文](README.md)

This repository provides a step-by-step options learning path with OpenBB Python examples, moving from core concepts to analysis and visualization.

## Overview
- Structured learning guide: basics → options core → Greeks → data practice → advanced projects
- Runnable OpenBB scripts for quotes, chains, Greeks, IV, visualization, and screening
- Sample output images (Greeks and volatility smile)

## Structure
- [`Options_Learning_and_OpenBB_Practice_Guide.md`](Options_Learning_and_OpenBB_Practice_Guide.md): full study notes and code snippets (English)
- `1-1 stock.py`: stock quote and historical prices
- `2-2 option chain.py`: option chain and expirations
- `2-2 option chain extra.py`: chain filtering and Greeks basics
- `3-5 greeks.py`: view Greeks data
- `4-1 option analyize.py`: options analysis workflow
- `4-2 greeks viz.py`: Greeks visualization
- `4-3 IV.py`: implied volatility smile
- `5-1 option screener.py`: high-IV options screener
- `5-2 option strategy viz.py`: option strategy payoff plot
- `greeks_correct.png`, `volatility_smile.png`: sample outputs

## Requirements
- Python 3.10+
- OpenBB installed (follow official docs)
- Recommended: virtual environment

## Quick Start
```powershell
# Option chain example
python ".\2-2 option chain.py"

# Greeks visualization
python ".\4-2 greeks viz.py"
```

> On Windows, quote paths that include spaces.

## Learning Path (Short)
1. Basics: stocks, derivatives
2. Options core: value components, status, expirations/DTE
3. Greeks: Delta/Gamma/Theta/Vega
4. Practice: chain filtering, Greeks/IV visualization
5. Projects: screener, payoff chart

## Notes
- Examples use `AAPL` and `SPY` by default; replace as needed.
- Data availability depends on OpenBB provider and permissions.

