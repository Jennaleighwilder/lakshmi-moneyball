"""
12 DOMAINS — Multi-market data for LAKSHMI
Each domain fetches, stores, learns. Eventually branches.
"""

DOMAINS = [
    "prediction",   # 1. Kalshi, Polymarket
    "sports",       # 2. Odds APIs
    "dfs",          # 3. PrizePicks, Underdog
    "esports",      # 4. Esports odds
    "stocks",       # 5. TESS + Yahoo (current)
    "crypto",       # 6. Spot, perps
    "insurance",    # 7. Cat bonds (funds)
    "casino",       # 8. House edge (skip for edge)
    "horses",       # 9. Pari-mutuel
    "sweeps",       # 10. Social casino (skip)
    "derivatives",  # 11. Futures, VIX
    "unusual",      # 12. Niche prediction
]
