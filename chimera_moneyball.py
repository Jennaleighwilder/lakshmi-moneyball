#!/usr/bin/env python3
"""
CHIMERA + LAKSHMI — Self-evolving analysis for the Moneyball system.
Uses Chimera's calculate_roi, basic_stats, predict_sales on portfolio & price data.
State: ~/lakshmi-moneyball/state/chimera_state.json
"""

import json
import os
from pathlib import Path
from datetime import datetime

BOT_DIR = Path(__file__).parent.resolve()
STATE_DIR = BOT_DIR / "state"
CHIMERA_STATE = STATE_DIR / "chimera_state.json"


def get_chimera():
    """Load Chimera engine, bootstrap money capabilities if needed."""
    import sys
    sys.path.insert(0, str(BOT_DIR))
    from engines.chimera_engine import ChimeraCoreEngine

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    engine = ChimeraCoreEngine(output_dir=str(STATE_DIR), quiet=True)

    # Bootstrap money capabilities if not present (Chimera has basic_stats; add ROI + predict)
    for name, desc in [
        ("calculate_roi", "Calculate return on investment for financial analysis"),
        ("predict_sales", "Generate sales forecasts based on historical data"),
    ]:
        if name not in engine.get_capabilities():
            try:
                engine.generate_capability(name, desc)
            except Exception:
                pass

    if os.path.exists(CHIMERA_STATE):
        engine.load_state(str(CHIMERA_STATE))
    return engine


def analyze_portfolio(engine, portfolio: dict, live_prices: dict) -> dict:
    """Use Chimera to analyze portfolio: ROI, stats, insights."""
    recs = portfolio.get("recommendations", [])
    if not recs:
        return {"status": "no_picks", "insights": []}

    # Build price history for stats (use live as latest)
    insights = []
    tickers = [r["ticker"] for r in recs]
    amounts = [r.get("amount", 10) for r in recs]

    # ROI for each pick if we have entry + current
    for r in recs:
        ticker = r["ticker"]
        amt = r.get("amount", 10)
        current = live_prices.get(ticker)
        if current and amt > 0:
            # Simulate: we "invested" $amt, current value = shares * price
            # We don't have shares, so assume we're tracking $ invested
            # For ROI we need entry price - use portfolio history or assume flat
            pass  # Skip ROI without history

    # Basic stats on confidence scores
    confs = [r.get("confidence", 0) for r in recs if r.get("confidence")]
    if confs:
        result = engine.execute_capability("basic_stats", confs)
        if result.get("success") and "error" not in str(result.get("result", {})):
            stats = result["result"]
            insights.append({
                "type": "stats",
                "text": f"TESS confidence: avg {stats.get('average', 0):.0f}, range {stats.get('min', 0)}–{stats.get('max', 0)}",
            })

    # Predict trend from confidence (Chimera predict_sales works on numeric lists)
    if len(confs) >= 2:
        result = engine.execute_capability("predict_sales", confs)
        if result.get("success") and "error" not in str(result.get("result", {})):
            pred = result["result"]
            insights.append({
                "type": "forecast",
                "text": f"Quality trend: {pred.get('growth_rate_percent', 0):.0f}% — {'improving' if pred.get('growth_rate_percent', 0) > 0 else 'stable'}",
            })

    return {
        "status": "ok",
        "insights": insights,
        "chimera_status": engine.get_status(),
    }


def save_chimera_state(engine):
    """Persist Chimera state."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    engine.save_state(str(CHIMERA_STATE))
