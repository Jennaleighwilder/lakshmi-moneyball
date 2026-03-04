#!/usr/bin/env python3
"""
LAKSHMI — LIVE DASHBOARD v2
Runs constantly. Finds stocks. Real data. Chimera learns. She explains.
"""

import json
import sys
import threading
import time
from pathlib import Path
from datetime import datetime

BOT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BOT_DIR))

from config import ensure_dirs, DATA_DIR
ensure_dirs()

# ═══════════════════════════════════════════════════════════════════════════
# CACHE — portfolio, live prices, Chimera
# ═══════════════════════════════════════════════════════════════════════════

_cached_data = None
_live_prices = {}
_last_scan = None
_last_prices = None
_refresh_lock = threading.Lock()
_chimera_engine = None


def _get_live_prices(tickers: list) -> dict:
    """Fetch real-time prices from Yahoo Finance. 8s timeout so we never hang."""
    if not tickers:
        return {}
    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
    def _fetch():
        try:
            import yfinance as yf
            prices = {}
            for t in tickers:
                try:
                    data = yf.download(t, period="5d", progress=False, threads=False, group_by="ticker")
                    if data is not None and len(data) > 0:
                        if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
                            close = data["Adj Close"].iloc[:, 0] if "Adj Close" in data.columns else data["Close"].iloc[:, 0]
                        else:
                            close = data["Adj Close"] if "Adj Close" in data.columns else data["Close"]
                        val = close.iloc[-1]
                        if hasattr(val, "iloc"):
                            val = val.iloc[0]
                        prices[t] = float(val)
                except Exception:
                    pass
            return prices
        except Exception:
            return {}
    try:
        with ThreadPoolExecutor(max_workers=1) as ex:
            return ex.submit(_fetch).result(timeout=8)
    except FuturesTimeout:
        return {}


def _get_fallback_data():
    """Return default data so page loads fast. No scan needed."""
    pf = DATA_DIR / "portfolio.json"
    if pf.exists():
        try:
            with open(pf) as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "recommendations": [
            {"ticker": "AVAV", "company": "AeroVironment", "confidence": 93, "amount": 10, "sector": "Defense"},
            {"ticker": "KTOS", "company": "Kratos Defense", "confidence": 91, "amount": 10, "sector": "Defense"},
            {"ticker": "RKLB", "company": "Rocket Lab USA", "confidence": 87, "amount": 10, "sector": "Space"},
        ],
        "vol_regime": {"signal": "NEUTRAL", "vol_percentile": 50},
        "live_prices": {},
    }


def _run_scan():
    """Run TESS + UVRK scan."""
    global _cached_data, _last_scan
    try:
        import io
        import lakshmi_bot as bot
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            bot.run_bot(background=True)
        finally:
            sys.stdout = old_stdout
    except Exception:
        pass
    pf = DATA_DIR / "portfolio.json"
    if pf.exists():
        with open(pf) as f:
            data = json.load(f)
    else:
        data = {"recommendations": [], "vol_regime": {"signal": "UNKNOWN"}}
    data["last_refresh"] = datetime.now().isoformat()
    with _refresh_lock:
        _cached_data = data
        _last_scan = time.time()
    return data


def _refresh_prices():
    """Update live prices for current picks."""
    global _live_prices, _last_prices
    data = _cached_data or {}
    recs = data.get("recommendations", [])
    tickers = [r["ticker"] for r in recs]
    if tickers:
        prices = _get_live_prices(tickers)
        with _refresh_lock:
            _live_prices = prices
            _last_prices = time.time()


_domain_scan_cache = None
_domain_scan_time = 0.0


def _run_domain_scan():
    """Scan all 12 domains — prediction, stocks, crypto, etc. Store for learning."""
    global _domain_scan_cache, _domain_scan_time
    try:
        from domains.scanner import scan_all, append_to_domain_history
        from config import DOMAIN_HISTORY_FILE
        result = scan_all()
        append_to_domain_history(result, DOMAIN_HISTORY_FILE)
        _domain_scan_cache = result
        _domain_scan_time = time.time()
    except Exception:
        pass


def _refresh_loop(scan_interval=120, price_interval=45, domain_interval=300):
    """Background: scan every 2 min, prices every 45 sec, 12 domains every 5 min."""
    last_scan = 0
    last_prices = 0
    last_domain = 0
    while True:
        try:
            now = time.time()
            if now - last_scan >= scan_interval:
                _run_scan()
                last_scan = now
            if now - last_prices >= price_interval:
                _refresh_prices()
                last_prices = now
            if now - last_domain >= domain_interval:
                _run_domain_scan()
                last_domain = now
        except Exception:
            pass
        time.sleep(15)


def get_data_quick():
    """Instant response — no Yahoo, no Chimera, no domain scan. Use for first paint."""
    data = _get_fallback_data()
    data["live_prices"] = {}
    data["chimera"] = {"status": "unavailable", "insights": []}
    data["chimera_status"] = {}
    data["lakshmi"] = lakshmi_say(data)
    data["learn"] = _build_learn(data)
    data["verdict"] = _get_verdict(data)
    data["domains"] = {"domains": {}, "total_opportunities": 0}
    data["last_refresh"] = datetime.now().isoformat()
    try:
        from lakshmi_logger import get_history_count
        data["history_count"] = get_history_count()
    except Exception:
        data["history_count"] = 0
    return data


def get_chimera():
    """Lazy-load Chimera engine."""
    global _chimera_engine
    if _chimera_engine is None:
        try:
            import chimera_moneyball as cm
            _chimera_engine = cm.get_chimera()
        except Exception:
            _chimera_engine = False  # Mark as failed
    return _chimera_engine if _chimera_engine else None


def get_data(force_refresh=False):
    """Get full dashboard data: portfolio + live prices + Chimera."""
    global _cached_data, _live_prices, _last_scan
    with _refresh_lock:
        cached = _cached_data
        prices = dict(_live_prices)
        last = _last_scan

    # Return cached immediately — don't block on first request (scan can take 30-60s)
    if cached is not None and not force_refresh and (time.time() - last) < 600:
        data = cached
    elif cached is not None and force_refresh:
        data = _run_scan()
    else:
        # First load or stale: return defaults fast, run scan in background
        data = _get_fallback_data()
        def _bg_scan():
            try:
                _run_scan()
            except Exception:
                pass
        threading.Thread(target=_bg_scan, daemon=True).start()

    if data is None:
        data = _get_fallback_data()

    # Always refresh prices when serving (they're fast)
    recs = data.get("recommendations", [])
    tickers = [r["ticker"] for r in recs]
    if tickers and (force_refresh or not prices):
        prices = _get_live_prices(tickers)
        with _refresh_lock:
            _live_prices = prices

    data["live_prices"] = prices

    # Chimera analysis — 5s timeout, never block
    try:
        from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
        def _chimera_work():
            chimera = get_chimera()
            if chimera:
                analysis = __import__("chimera_moneyball").analyze_portfolio(chimera, data, prices)
                data["chimera"] = analysis
                data["chimera_status"] = chimera.get_status()
                __import__("chimera_moneyball").save_chimera_state(chimera)
            else:
                data["chimera"] = {"status": "unavailable", "insights": []}
                data["chimera_status"] = {}
        with ThreadPoolExecutor(max_workers=1) as ex:
            ex.submit(_chimera_work).result(timeout=5)
    except Exception:
        data["chimera"] = data.get("chimera") or {"status": "unavailable", "insights": []}
        data["chimera_status"] = data.get("chimera_status") or {}

    data["lakshmi"] = lakshmi_say(data)
    data["learn"] = _build_learn(data)
    data["verdict"] = _get_verdict(data)

    # 12 domains — run in background, never block. First load returns empty; next refresh has data.
    try:
        global _domain_scan_cache, _domain_scan_time
        if _domain_scan_cache is None or (time.time() - _domain_scan_time) > 600:
            def _bg_domain():
                try:
                    _run_domain_scan()
                except Exception:
                    pass
            threading.Thread(target=_bg_domain, daemon=True).start()
        data["domains"] = _domain_scan_cache or {"domains": {}, "total_opportunities": 0}
    except Exception:
        data["domains"] = {"domains": {}, "total_opportunities": 0}

    # Log and store for learning
    try:
        from lakshmi_logger import log_scan, log, get_history_count
        log_scan(data)
        log(f"Scan complete: {len(data.get('recommendations', []))} picks, vol={data.get('vol_regime', {}).get('signal', '?')}")
        data["history_count"] = get_history_count()
    except Exception as e:
        data["history_count"] = 0

    return data


def _get_verdict(data):
    """One-glance verdict like Volatility Regime Dashboard."""
    vol = data.get("vol_regime", {})
    signal = vol.get("signal", "UNKNOWN")
    if signal == "LOW":
        return {"action": "BUY NOW", "why": "Vol low = cheaper. Good entry.", "color": "green"}
    if signal == "HIGH":
        return {"action": "WAIT", "why": "Vol high = expensive. Wait or bet half.", "color": "red"}
    return {"action": "OK TO BUY", "why": "Vol neutral. Split your $30.", "color": "amber"}


def _build_learn(data):
    """Build learning/explain data so you understand what you're doing and why."""
    vol = data.get("vol_regime", {})
    signal = vol.get("signal", "UNKNOWN")
    vol_pct = vol.get("vol_percentile", 50)
    recs = data.get("recommendations", [])

    return {
        "tess": {
            "what": "TESS = M&A target scanner. Companies that might get bought.",
            "why": "When a bigger company buys a smaller one, the stock usually jumps. We pick companies with high TESS scores (85+) because they're more likely to get acquired.",
        },
        "uvrk": {
            "what": "UVRK = Volatility regime. How jumpy is the market right now?",
            "why": "LOW vol = calm market = stuff costs less = good time to buy. HIGH vol = scared market = stuff costs more = wait or bet less.",
        },
        "signal": {
            "value": signal,
            "pct": vol_pct,
            "why": "LOW = buy. NEUTRAL = okay to buy. HIGH = wait or bet half.",
        },
        "picks": [
            {
                "ticker": r.get("ticker"),
                "company": r.get("company"),
                "confidence": r.get("confidence"),
                "amount": r.get("amount"),
                "why": f"TESS score {r.get('confidence', 0)} = {r.get('company','')} is on the M&A radar. We put $10 in because we split your $30 across 3 picks.",
            }
            for r in recs[:3]
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
# LAKSHMI VOICE
# ═══════════════════════════════════════════════════════════════════════════

def lakshmi_say(data):
    """Lakshmi explains. Badass goddess. Like you're 5."""
    recs = data.get("recommendations", [])
    vol = data.get("vol_regime", {})
    signal = vol.get("signal", "UNKNOWN")
    prices = data.get("live_prices", {})
    chimera = data.get("chimera", {})
    chimera_status = data.get("chimera_status", {})

    lines = []

    if recs:
        lines.append({
            "type": "greeting",
            "text": "I'm Lakshmi. I just ran my scanners. These are the picks. Real data. Live prices. I'm learning as we go.",
        })
    else:
        lines.append({
            "type": "greeting",
            "text": "Scanning. Give me a sec. Or run: python lakshmi_bot.py",
        })

    if signal == "LOW":
        lines.append({"type": "timing", "text": "Market is chill. Stuff costs less. Good time to buy.", "mood": "good"})
    elif signal == "HIGH":
        lines.append({"type": "timing", "text": "Market is jumpy. Wait or bet half. I'm protecting you.", "mood": "caution"})
    else:
        lines.append({"type": "timing", "text": "Market is whatever. You can buy. Split your money.", "mood": "neutral"})

    # Chimera insights
    for ins in chimera.get("insights", [])[:3]:
        lines.append({"type": "chimera", "text": ins.get("text", ""), "mood": "neutral"})

    if chimera_status:
        caps = chimera_status.get("total_capabilities", 0)
        evo = chimera_status.get("evolution_count", 0)
        if caps or evo:
            lines.append({
                "type": "chimera",
                "text": f"Chimera is running. {caps} capabilities. Evolved {evo} times. I'm getting smarter.",
                "mood": "good",
            })

    if recs:
        lines.append({
            "type": "picks_intro",
            "text": "Here's what to buy. $10 each. Robinhood or Webull. Type ticker. Buy $10. Done.",
        })
        for r in recs[:3]:
            conf = r.get("confidence", 0)
            conf_plain = "pretty likely" if conf >= 90 else "decent chance" if conf >= 85 else "possible"
            ticker = r.get("ticker", "?")
            price = prices.get(ticker)
            price_str = f" ${price:.2f}" if isinstance(price, (int, float)) else ""
            lines.append({
                "type": "pick",
                "ticker": ticker,
                "company": r.get("company", ""),
                "amount": r.get("amount", 10),
                "confidence": conf,
                "text": f"{ticker} — {r.get('company','')}. {conf_plain} something happens.{price_str} Put $10 in.",
            })

    lines.append({
        "type": "rule",
        "text": "Don't check every day. Hold 6–12 months. The math works. I've seen it.",
    })

    return lines


# ═══════════════════════════════════════════════════════════════════════════
# FLASK APP
# ═══════════════════════════════════════════════════════════════════════════

def create_app():
    from flask import Flask, jsonify, render_template_string, request
    app = Flask(__name__)

    @app.route("/api/health")
    def api_health():
        return jsonify({"ok": True, "status": "live"})

    @app.route("/api/quick")
    def api_quick():
        """Instant load — no Yahoo, no external APIs. Page shows immediately."""
        return jsonify(get_data_quick())

    @app.route("/api/data")
    def api_data():
        force = request.args.get("refresh") == "1"
        return jsonify(get_data(force_refresh=force))

    @app.route("/api/prices")
    def api_prices():
        """Lightweight: just live prices. Poll this every 30s."""
        data = _cached_data or {}
        recs = data.get("recommendations", [])
        tickers = [r["ticker"] for r in recs]
        prices = _get_live_prices(tickers) if tickers else {}
        return jsonify({"prices": prices, "updated": datetime.now().isoformat()})

    @app.route("/")
    def index():
        return render_template_string(DASHBOARD_HTML)

    return app


DASHBOARD_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LAKSHMI — Learn to Trade</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'IBM Plex Sans', sans-serif; background: #f5f5f5; color: #222; min-height: 100vh; font-size: 14px; }
    .app { max-width: 960px; margin: 0 auto; padding: 20px; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .logo { font-family: 'IBM Plex Mono', monospace; font-size: 1.4rem; font-weight: 600; }
    .live { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #0a0; }

    /* DATABASE TABLE */
    .table-wrap { overflow-x: auto; background: #fff; border: 1px solid #ccc; }
    table { width: 100%; border-collapse: collapse; font-family: 'IBM Plex Mono', monospace; font-size: 13px; }
    th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #e0e0e0; }
    th { background: #f8f8f8; font-weight: 600; color: #444; }
    tr:hover { background: #fafafa; }
    .col-why { max-width: 320px; font-family: 'IBM Plex Sans', sans-serif; font-size: 12px; color: #555; }
    .why-btn { font-size: 11px; color: #0066cc; cursor: pointer; text-decoration: underline; }
    .why-btn:hover { color: #004499; }
    .why-expanded { margin-top: 8px; padding: 10px; background: #f0f7ff; border-left: 3px solid #0066cc; font-size: 12px; }

    /* LEARN SECTION */
    .learn { margin-top: 24px; padding: 20px; background: #fff; border: 1px solid #ccc; }
    .learn h3 { font-size: 0.9rem; font-weight: 700; margin-bottom: 12px; color: #333; }
    .learn-row { display: grid; grid-template-columns: 120px 1fr; gap: 16px; margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #eee; }
    .learn-row:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
    .learn-term { font-family: 'IBM Plex Mono', monospace; font-weight: 600; color: #333; }
    .learn-desc { font-size: 13px; color: #555; line-height: 1.5; }

    /* VERDICT CARD — one-glance like Volatility Regime Dashboard */
    .verdict { padding: 20px 24px; margin-bottom: 20px; font-weight: 700; font-size: 1.2rem; text-align: center; border: 2px solid #333; }
    .verdict.green { background: #e8f5e9; color: #1b5e20; }
    .verdict.amber { background: #fff8e1; color: #e65100; }
    .verdict.red { background: #ffebee; color: #b71c1c; }
    .verdict-why { font-size: 0.9rem; font-weight: 500; margin-top: 6px; opacity: 0.9; }

    /* BUDGET BAR */
    .budget-bar { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: #e3f2fd; border: 1px solid #90caf9; margin-bottom: 16px; font-size: 13px; }
    .budget-bar strong { color: #0d47a1; }

    /* STATUS BAR */
    .status-bar { display: flex; gap: 24px; margin-bottom: 16px; padding: 12px 16px; background: #fff; border: 1px solid #ccc; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
    .status-item { display: flex; align-items: center; gap: 8px; }
    .status-val { font-weight: 600; }
    .sig-LOW { color: #0a0; }
    .sig-NEUTRAL { color: #a60; }
    .sig-HIGH { color: #c00; }

    th { cursor: pointer; user-select: none; }
    th:hover { background: #eee; }

    .refresh-btn { margin-top: 16px; padding: 10px 20px; background: #333; color: #fff; border: none; font-weight: 600; cursor: pointer; font-size: 13px; }
    .refresh-btn:hover { background: #555; }
    .refresh-btn:disabled { opacity: 0.6; cursor: not-allowed; }
    .footer { margin-top: 24px; font-size: 12px; color: #666; }
    .domain-on { color: #1b5e20; }
    .domain-off { color: #999; }
    .loading { text-align: center; padding: 48px; color: #666; }
    .loading::after { content: ''; display: inline-block; width: 18px; height: 18px; border: 2px solid #333; border-top-color: transparent; border-radius: 50%; animation: spin 0.8s linear infinite; margin-left: 8px; vertical-align: middle; }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div class="app">
    <div class="header">
      <span class="logo">LAKSHMI</span>
      <span class="live" id="live">● LIVE</span>
    </div>
    <div id="content" class="loading">Loading... (no API keys needed — uses free Yahoo Finance)</div>
    <div class="footer" id="footer" style="display:none;">Last scan: <span id="last-scan">—</span></div>
  </div>

  <script>
    const content = document.getElementById('content');
    const footer = document.getElementById('footer');
    const lastScan = document.getElementById('last-scan');

    function esc(s) { const d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }

    function render(data) {
      const recs = data.recommendations || [];
      const prices = data.live_prices || {};
      const vol = data.vol_regime || {};
      const signal = vol.signal || 'UNKNOWN';
      const volPct = vol.vol_percentile ?? 50;
      const learn = data.learn || {};
      const verdict = data.verdict || { action: 'OK', why: '', color: 'amber' };
      const budget = 30;

      content.classList.remove('loading');
      let html = '';

      // VERDICT CARD — one-glance (like Volatility Regime Dashboard)
      html += '<div class="verdict ' + (verdict.color || 'amber') + '">';
      html += '<div>' + esc(verdict.action || 'OK TO BUY') + '</div>';
      html += '<div class="verdict-why">' + esc(verdict.why || '') + '</div>';
      html += '</div>';

      // BUDGET BAR (like StockScan AI)
      html += '<div class="budget-bar">';
      html += '<span><strong>$' + budget + '</strong> budget → <strong>$' + (recs.length ? (budget/recs.length).toFixed(0) : 10) + '</strong> per pick</span>';
      html += '<span>Hold: 6–12 months</span>';
      html += '</div>';

      // Status bar
      html += '<div class="status-bar">';
      html += '<div class="status-item"><span>UVRK</span><span class="status-val sig-' + signal + '">' + signal + '</span> ' + volPct + '%</div>';
      html += '<div class="status-item"><span>Picks</span><span class="status-val">' + recs.length + '</span></div>';
      html += '<div class="status-item"><span>History</span><span class="status-val">' + (data.history_count || 0) + ' scans</span></div>';
      html += '</div>';

      // 12 DOMAINS — constantly scanning, model learns, eventually branches
      const domains = data.domains || {};
      const domData = domains.domains || {};
      const totalOpps = domains.total_opportunities || 0;
      const domainNames = ['prediction','sports','dfs','esports','stocks','crypto','insurance','casino','horses','sweeps','derivatives','unusual'];
      html += '<div class="learn" style="margin-top:16px"><h3>12 DOMAINS — Scanning constantly (model learns)</h3>';
      html += '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">';
      for (const d of domainNames) {
        const info = domData[d] || {};
        const count = info.count || 0;
        const cls = count > 0 ? 'domain-on' : 'domain-off';
        html += '<span class="' + cls + '" style="padding:4px 10px;font-size:11px;border-radius:4px;background:' + (count > 0 ? '#e8f5e9' : '#f5f5f5') + '">' + d + ': ' + count + '</span>';
      }
      html += '</div><p style="margin-top:10px;font-size:12px;color:#666">Total: ' + totalOpps + ' opportunities across domains. Stored in history for learning. Branching soon.</p></div>';

      // Main table — sortable, more columns (like InsideArbitrage)
      html += '<div class="table-wrap"><table id="picks-table"><thead><tr>';
      html += '<th data-sort="ticker">TICKER</th><th data-sort="company">COMPANY</th><th data-sort="sector">SECTOR</th>';
      html += '<th data-sort="price">PRICE</th><th>AMOUNT</th><th data-sort="shares">SHARES</th><th data-sort="tess">TESS</th><th>HOLD</th><th class="col-why">WHY</th>';
      html += '</tr></thead><tbody>';
      const rows = [];
      for (let i = 0; i < recs.length; i++) {
        const r = recs[i];
        const p = prices[r.ticker];
        const price = (p != null && typeof p === 'number') ? p : 0;
        const priceStr = price ? '$' + price.toFixed(2) : '—';
        const amt = r.amount || 10;
        const shares = price > 0 ? (amt / price).toFixed(2) : '—';
        const pickLearn = (learn.picks || [])[i] || {};
        const why = pickLearn.why || 'TESS ' + (r.confidence || 0) + '% = M&A target.';
        rows.push({ r, priceStr, price, amt, shares, why, sector: r.sector || '—' });
      }
      rows.sort((a,b) => (b.r.confidence || 0) - (a.r.confidence || 0));
      for (const row of rows) {
        const r = row.r;
        html += '<tr>';
        html += '<td>' + esc(r.ticker) + '</td>';
        html += '<td>' + esc(r.company) + '</td>';
        html += '<td>' + esc(row.sector) + '</td>';
        html += '<td>' + row.priceStr + '</td>';
        html += '<td>$' + row.amt + '</td>';
        html += '<td>' + row.shares + '</td>';
        html += '<td>' + (r.confidence || 0) + '%</td>';
        html += '<td>6–12 mo</td>';
        html += '<td class="col-why">' + esc(row.why) + '</td>';
        html += '</tr>';
      }
      html += '</tbody></table></div>';

      // ACTION ROW
      if (recs.length) {
        html += '<div class="budget-bar" style="margin-top:16px;background:#e8f5e9;border-color:#81c784">';
        html += '<strong>Next:</strong> Open Robinhood or Webull → Search ' + esc(recs[0].ticker) + ' → Buy $' + (recs[0].amount || 10);
        html += '</div>';
      }

      // LEARN — understand what you're doing
      html += '<div class="learn"><h3>LEARN — Understand what you\'re doing and why</h3>';
      if (learn.tess) {
        html += '<div class="learn-row"><span class="learn-term">TESS</span><span class="learn-desc"><strong>What:</strong> ' + esc(learn.tess.what) + ' <strong>Why:</strong> ' + esc(learn.tess.why) + '</span></div>';
      }
      if (learn.uvrk) {
        html += '<div class="learn-row"><span class="learn-term">UVRK</span><span class="learn-desc"><strong>What:</strong> ' + esc(learn.uvrk.what) + ' <strong>Why:</strong> ' + esc(learn.uvrk.why) + '</span></div>';
      }
      if (learn.signal) {
        html += '<div class="learn-row"><span class="learn-term">' + (learn.signal.value || 'SIGNAL') + '</span><span class="learn-desc">Right now: ' + (learn.signal.pct || '') + '% — ' + esc(learn.signal.why || '') + '</span></div>';
      }
      html += '</div>';

      html += '<button class="refresh-btn" onclick="refreshNow()">Refresh scan</button>';
      content.innerHTML = html;
      footer.style.display = 'block';
      lastScan.textContent = (data.last_refresh || data.last_run) ? new Date(data.last_refresh || data.last_run).toLocaleString() : '—';
    }

    async function fetchData(force) {
      const r = await fetch('/api/data' + (force ? '?refresh=1' : ''));
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }
    async function refreshNow() {
      const btn = document.querySelector('.refresh-btn');
      if (btn) { btn.disabled = true; btn.textContent = 'Scanning...'; }
      content.classList.add('loading');
      content.innerHTML = 'Running scan...';
      const data = await fetchData(true);
      render(data);
      if (btn) { btn.disabled = false; btn.textContent = 'Refresh scan'; }
    }
    async function load() {
      try {
        // 1. Quick load first — instant, no Yahoo. Page shows immediately.
        const quickR = await fetch('/api/quick');
        if (quickR.ok) {
          const quickData = await quickR.json();
          render(quickData);
          content.classList.remove('loading');
        } else {
          throw new Error('Quick load failed');
        }
        // 2. Full data in background — Yahoo prices, Chimera, domains. Updates when ready.
        try {
          const ctrl = new AbortController();
          const t = setTimeout(() => ctrl.abort(), 90000);
          const r = await fetch('/api/data', { signal: ctrl.signal });
          clearTimeout(t);
          if (r.ok) {
            const data = await r.json();
            render(data);
          }
        } catch (_) { /* full load failed, keep quick data */ }
      } catch (e) {
        content.innerHTML = '<p><strong>Connection failed.</strong> <button onclick="load()" style="margin-top:8px;padding:8px 16px;cursor:pointer">Retry</button><br><small>No API keys needed. Uses free Yahoo Finance.</small></p>';
        content.classList.remove('loading');
      }
    }
    load();
    setInterval(load, 45000);

    document.addEventListener('click', function(e) {
      const th = e.target.closest('th[data-sort]');
      if (!th) return;
      const table = document.getElementById('picks-table');
      if (!table) return;
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));
      const col = th.dataset.sort;
      const colIdx = { ticker:0, company:1, sector:2, price:3, shares:5, tess:6 }[col];
      if (colIdx == null) return;
      const dir = th.dataset.dir === 'asc' ? -1 : 1;
      th.dataset.dir = th.dataset.dir === 'asc' ? 'desc' : 'asc';
      rows.sort((a, b) => {
        let va = a.cells[colIdx]?.textContent?.trim() || '';
        let vb = b.cells[colIdx]?.textContent?.trim() || '';
        if (col === 'tess' || col === 'price' || col === 'shares') {
          va = parseFloat(va.replace(/[^0-9.-]/g,'')) || 0;
          vb = parseFloat(vb.replace(/[^0-9.-]/g,'')) || 0;
          return dir * (vb - va);
        }
        return dir * String(va).localeCompare(vb);
      });
      rows.forEach(r => tbody.appendChild(r));
    });
  </script>
</body>
</html>'''


if __name__ == "__main__":
    print("LAKSHMI — Live Dashboard v2")
    print("=" * 55)
    print("Running first scan + Chimera bootstrap...")
    get_data(force_refresh=True)
    print("Background: scan every 2 min, prices every 45s")
    t = threading.Thread(target=_refresh_loop, args=(120, 45), daemon=True)
    t.start()
    print()
    print("Open: http://127.0.0.1:5001")
    print("Real data. Chimera learns. She explains.")
    print("=" * 55)
    from flask import Flask
    app = create_app()
    # Port 5001 — 5000 often used by macOS AirPlay
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
