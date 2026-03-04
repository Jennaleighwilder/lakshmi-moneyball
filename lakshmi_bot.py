#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        LAKSHMI MONEYBALL BOT                                ║
║                                                                              ║
║   TESS (M&A targets) + UVRK (volatility) = What to buy, when, how much      ║
║                                                                              ║
║   Run: python lakshmi_bot.py                                                 ║
║   Background: python lakshmi_bot.py --background                             ║
║                                                                              ║
║   © 2026 Jennifer Leigh West • The Forgotten Code Research Institute         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import math
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict, Optional

# Paths — use config for portable storage (Railway volume)
from config import DATA_DIR, LOGS_DIR, ensure_dirs
ensure_dirs()
HOME = Path.home()
BOT_DIR = Path(__file__).parent.resolve()
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"
BUY_LIST_FILE = BOT_DIR / "BUY_NOW.md"

# TESS data paths (try multiple locations)
TESS_PATHS = [
    HOME / "Downloads" / "files" / "data" / "TESS_MASTER_GLOBAL_DATABASE.csv",
    HOME / "Downloads" / "TESS_1000_Deals_Package" / "TESS_Master_1000_Deals.csv",
    BOT_DIR / "TESS_MASTER_GLOBAL_DATABASE.csv",
]

# Company name -> Yahoo Finance ticker (US public companies from TESS)
TESS_TO_TICKER = {
    "LPL Financial": "LPLA",
    "Fifth Third Bancorp": "FITB",
    "Comerica Inc": "CMA",
    "Pinnacle Financial Partners": "PNFP",
    "M&T Bank": "MTB",
    "First Horizon": "FHN",
    "Freeport-McMoRan": "FCX",
    "MP Materials": "MP",
    "Energy Fuels": "UUUU",
    "Lithium Americas": "LAC",
    "Piedmont Lithium": "PLL",
    "Sigma Lithium": "SGML",
    "Kratos Defense & Security": "KTOS",
    "AeroVironment": "AVAV",
    "Rocket Lab USA": "RKLB",
    "Velo3D": "VLD",
    "GlobalFoundries": "GFS",
    "Tower Semiconductor": "TSEM",
    "Lattice Semiconductor": "LSCC",
    "Amkor Technology": "AMKR",
    "Vertiv Holdings": "VRT",
    "Western Digital": "WDC",
    "Wolfspeed": "WOLF",
    "Viking Therapeutics": "VKTX",
    "Structure Therapeutics": "GPCR",
    "Ventyx Biosciences": "VTYX",
    "Revolution Medicines": "RVMD",
    "Terns Pharmaceuticals": "TERN",
    "Xenon Pharmaceuticals": "XENE",
    "Chesapeake Energy": "CHK",
    "EQT Corporation": "EQT",
    "NextDecade Corporation": "NEXT",
    "California Water Service": "CWT",
    "Elbit Systems": "ESLT",
    "First Quantum Minerals": "FQVLF",
    "Lundin Mining": "LUNMF",
}

# ═══════════════════════════════════════════════════════════════════════════════
# UVRK-1 (from your validation script)
# ═══════════════════════════════════════════════════════════════════════════════

def probit(p: float) -> float:
    if p <= 0: p = 0.0001
    if p >= 1: p = 0.9999
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]
    p_low = 0.02425
    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    elif p <= 1 - p_low:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5])*q / (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)


def rolling_volatility(prices: List[float], window: int = 20) -> List[float]:
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] > 0 and prices[i] > 0:
            returns.append(math.log(prices[i] / prices[i-1]))
    vols = []
    for i in range(window, len(returns)):
        chunk = returns[i-window:i]
        mean = sum(chunk) / len(chunk)
        var = sum((x - mean)**2 for x in chunk) / len(chunk)
        vols.append(math.sqrt(var) * math.sqrt(252))
    return vols


def compute_rank(value: float, history: List[float]) -> float:
    if not history:
        return 0.5
    below = sum(1 for v in history if v < value)
    return max(0.001, min(0.999, below / len(history)))


def get_vol_regime(ticker: str = "SPY") -> Dict:
    """Get current volatility regime for a ticker. Returns vol level and trend."""
    try:
        import yfinance as yf
        import pandas as pd
        data = yf.download(ticker, period="1y", progress=False, threads=False)
        if data is None or len(data) < 60:
            return {"status": "no_data", "vol_percentile": 50}
        
        # Handle yfinance DataFrame structure (single vs multi ticker)
        if hasattr(data.columns, 'nlevels') and data.columns.nlevels > 1:
            price_series = data["Adj Close"].iloc[:, 0] if "Adj Close" in data.columns else data["Close"].iloc[:, 0]
        else:
            price_series = data["Adj Close"] if "Adj Close" in data.columns else data["Close"]
        prices = price_series.dropna().astype(float).tolist()
        vols = rolling_volatility(prices, 20)
        if len(vols) < 30:
            return {"status": "insufficient", "vol_percentile": 50}
        
        current_vol = vols[-1]
        vol_percentile = sum(1 for v in vols if v < current_vol) / len(vols) * 100
        
        return {
            "status": "ok",
            "current_vol": round(current_vol, 4),
            "vol_percentile": round(vol_percentile, 1),
            "signal": "LOW" if vol_percentile < 40 else "HIGH" if vol_percentile > 60 else "NEUTRAL",
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "vol_percentile": 50}


# ═══════════════════════════════════════════════════════════════════════════════
# TESS LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_tess_targets() -> List[Dict]:
    """Load TESS M&A targets. Returns list of {company, confidence, status, sector, ticker}."""
    targets = []
    
    for tess_path in TESS_PATHS:
        if not tess_path.exists():
            continue
        try:
            with open(tess_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    company = row.get("Company", row.get("Target", "")).strip()
                    if not company:
                        continue
                    conf_str = row.get("Confidence", row.get("Score", "0"))
                    try:
                        confidence = int(float(str(conf_str).replace(",", "")))
                    except:
                        confidence = 0
                    status = row.get("Status", row.get("Result", "Active")).strip()
                    sector = row.get("Sector", row.get("Sector_Category", "")).strip()
                    
                    # Skip completed/announced (already priced in)
                    if any(x in status.upper() for x in ["COMPLETED", "ACQUIRED", "ANNOUNCED", "MERGER", "BEING ACQUIRED"]):
                        continue
                    if "Active" not in status and "Public" not in status and "Rumored" not in status:
                        continue
                    
                    ticker = TESS_TO_TICKER.get(company)
                    if not ticker:
                        for key in TESS_TO_TICKER:
                            if key.lower() in company.lower() or company.lower() in key.lower():
                                ticker = TESS_TO_TICKER[key]
                                break
                    
                    if confidence >= 85 and ticker:
                        targets.append({
                            "company": company,
                            "confidence": confidence,
                            "status": status,
                            "sector": sector,
                            "ticker": ticker,
                        })
        except Exception as e:
            pass
    
    # Dedupe by ticker, keep highest confidence
    seen = {}
    for t in targets:
        tk = t["ticker"]
        if tk not in seen or t["confidence"] > seen[tk]["confidence"]:
            seen[tk] = t
    return sorted(seen.values(), key=lambda x: -x["confidence"])


# ═══════════════════════════════════════════════════════════════════════════════
# DEFAULT BUY LIST (when TESS file not found)
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_BUYS = [
    {"ticker": "LAC", "company": "Lithium Americas", "confidence": 91, "sector": "Critical Minerals"},
    {"ticker": "VTYX", "company": "Ventyx Biosciences", "confidence": 88, "sector": "Biotech"},
    {"ticker": "RKLB", "company": "Rocket Lab USA", "confidence": 87, "sector": "Defense/Space"},
    {"ticker": "KTOS", "company": "Kratos Defense", "confidence": 91, "sector": "Defense"},
    {"ticker": "MP", "company": "MP Materials", "confidence": 92, "sector": "Rare Earths"},
    {"ticker": "VKTX", "company": "Viking Therapeutics", "confidence": 92, "sector": "Biotech GLP-1"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# PORTFOLIO TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

def load_portfolio() -> Dict:
    if PORTFOLIO_FILE.exists():
        with open(PORTFOLIO_FILE) as f:
            return json.load(f)
    return {
        "start_date": datetime.now().isoformat()[:10],
        "start_cash": 30.0,
        "holdings": [],
        "history": [],
    }


def save_portfolio(data: Dict):
    PORTFOLIO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_current_prices(tickers: List[str]) -> Dict[str, float]:
    try:
        import yfinance as yf
        prices = {}
        for t in tickers:
            try:
                data = yf.download(t, period="5d", progress=False, threads=False)
                if data is not None and len(data) > 0:
                    close = data["Adj Close"] if "Adj Close" in data.columns else data["Close"]
                    if hasattr(close, 'iloc'):
                        val = close.iloc[-1]
                        if hasattr(val, 'iloc'):
                            val = val.iloc[0]
                        prices[t] = float(val)
                    else:
                        prices[t] = float(close[-1])
            except:
                pass
        return prices
    except:
        return {}


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN BOT
# ═══════════════════════════════════════════════════════════════════════════════

def run_bot(background: bool = False):
    global pd
    try:
        import pandas as pd
    except ImportError:
        print("Installing pandas...")
        os.system(f"{sys.executable} -m pip install pandas yfinance -q")
        import pandas as pd
    
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    print()
    print("=" * 60)
    print("  LAKSHMI MONEYBALL — TESS + UVRK")
    print("=" * 60)
    print()
    
    # 1. Load TESS targets
    targets = load_tess_targets()
    if not targets:
        targets = [{"ticker": b["ticker"], "company": b["company"], "confidence": b["confidence"], "sector": b["sector"]} for b in DEFAULT_BUYS]
        print("  Using default TESS targets (data file not found)")
    else:
        print(f"  TESS: {len(targets)} high-confidence targets")
    print()
    
    # 2. Get UVRK regime (SPY)
    print("  UVRK: Checking volatility regime (SPY)...")
    vol_regime = get_vol_regime("SPY")
    if vol_regime.get("status") == "ok":
        sig = vol_regime["signal"]
        pct = vol_regime["vol_percentile"]
        print(f"         Vol percentile: {pct}% → {sig}")
        if sig == "LOW":
            print("         ✓ Good entry (vol low = cheaper)")
        elif sig == "HIGH":
            print("         ⚠ Vol elevated — consider waiting or smaller size")
    else:
        print("         (Could not fetch — assume NEUTRAL)")
    print()
    
    # 3. Build buy list (top 6 for $30 = $5 each, or top 3 = $10 each)
    budget = 30.0
    n_picks = 3
    per_pick = budget / n_picks
    
    recommendations = targets[:6]
    
    # 4. Get current prices
    tickers = [r["ticker"] for r in recommendations]
    prices = get_current_prices(tickers)
    
    # 5. Build BUY_NOW.md
    buy_lines = [
        "# LAKSHMI MONEYBALL — BUY NOW",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Budget:** ${budget:.0f}",
        "",
        "## Your $30 Split (3 picks × $10)",
        "",
        "| # | Ticker | Company | TESS | Price | Amount |",
        "|---|--------|---------|------|-------|-------|",
    ]
    
    for i, rec in enumerate(recommendations[:3], 1):
        ticker = rec["ticker"]
        price = prices.get(ticker, 0)
        amt = per_pick
        shares = amt / price if price > 0 else 0
        buy_lines.append(f"| {i} | {ticker} | {rec['company']} | {rec['confidence']} | ${price:.2f} | ${amt:.0f} |")
    
    buy_lines.extend([
        "",
        "## Where to Buy",
        "- **Robinhood** — fractional shares, $0 commission",
        "- **Webull** — fractional shares",
        "- **Fidelity** — fractional",
        "",
        "## Hold Period",
        "6–12 months. TESS targets typically see M&A in that window.",
        "",
        "## Full Watchlist (if you add more later)",
    ])
    
    for rec in recommendations:
        ticker = rec["ticker"]
        price = prices.get(ticker, "?")
        pstr = f"${price:.2f}" if isinstance(price, (int, float)) else str(price)
        buy_lines.append(f"- **{ticker}** — {rec['company']} (TESS {rec['confidence']}) — {pstr}")
    
    BUY_LIST_FILE.write_text("\n".join(buy_lines), encoding="utf-8")
    print(f"  ✓ Wrote {BUY_LIST_FILE.name}")
    print()
    
    # 6. Update portfolio template
    portfolio = load_portfolio()
    portfolio["last_run"] = datetime.now().isoformat()
    portfolio["recommendations"] = [
        {"ticker": r["ticker"], "company": r["company"], "confidence": r["confidence"], "amount": per_pick}
        for r in recommendations[:3]
    ]
    portfolio["vol_regime"] = vol_regime
    save_portfolio(portfolio)
    
    # 7. Print summary
    print("=" * 60)
    print("  BUY THESE (with your $30):")
    print("=" * 60)
    for i, rec in enumerate(recommendations[:3], 1):
        ticker = rec["ticker"]
        price = prices.get(ticker, "?")
        print(f"  {i}. {ticker} — {rec['company']} — TESS {rec['confidence']} — ${per_pick:.0f}")
    print()
    print("  Open Robinhood/Webull → Buy $10 of each (fractional)")
    print()
    print("=" * 60)
    print("  Background bot: add to crontab for daily runs")
    print("  0 9 * * * cd ~/lakshmi-moneyball && python3 lakshmi_bot.py --background")
    print("=" * 60)
    print()


if __name__ == "__main__":
    background = "--background" in sys.argv
    run_bot(background=background)
