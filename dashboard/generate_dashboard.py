#!/usr/bin/env python3
"""Generate LAKSHMI Betting Dashboard — Beautiful, accessible, every step explained."""

import json
import sys
from pathlib import Path

BOT_DIR = Path(__file__).parent.parent
PORTFOLIO = BOT_DIR / "portfolio.json"
OUTPUT = Path(__file__).parent / "index.html"


def run_bot_first():
    try:
        sys.path.insert(0, str(BOT_DIR))
        import lakshmi_bot
        lakshmi_bot.run_bot(background=False)
    except Exception:
        pass


def load_data():
    if PORTFOLIO.exists():
        with open(PORTFOLIO) as f:
            return json.load(f)
    return {"recommendations": [], "vol_regime": {"signal": "UNKNOWN"}}


def generate_html(data):
    recs = data.get("recommendations", [])
    vol = data.get("vol_regime", {})
    signal = vol.get("signal", "UNKNOWN")
    vol_pct = vol.get("vol_percentile", 50)

    rec_html = ""
    for r in recs:
        rec_html += f'''
      <div class="pick">
        <span class="pick-ticker">{r.get('ticker','?')}</span>
        <span class="pick-name">{r.get('company','')}</span>
        <span class="pick-amt">${r.get('amount',0):.0f}</span>
      </div>'''
    if not rec_html:
        rec_html = '<p style="color:#7a756d;">Run the system first to get picks. (python lakshmi_system.py)</p>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LAKSHMI — Your Betting Guide</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'DM Sans', system-ui, -apple-system, sans-serif;
      background: linear-gradient(165deg, #f8f6f2 0%, #efe9e1 100%);
      color: #2d2a26;
      min-height: 100vh;
      line-height: 1.7;
      font-size: 18px;
      letter-spacing: 0.02em;
    }}
    .page {{ max-width: 560px; margin: 0 auto; padding: 48px 24px; }}
    
    .logo {{
      font-size: 1.25rem;
      font-weight: 700;
      color: #5c7c6b;
      margin-bottom: 8px;
    }}
    .tagline {{
      font-size: 1rem;
      color: #7a756d;
      margin-bottom: 48px;
    }}

    .section {{
      margin-bottom: 48px;
    }}
    .section-title {{
      font-size: 0.9rem;
      font-weight: 600;
      color: #5c7c6b;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 16px;
    }}

    .step {{
      background: white;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 16px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      border: 1px solid rgba(0,0,0,0.04);
    }}
    .step-num {{
      display: inline-block;
      width: 36px;
      height: 36px;
      background: #5c7c6b;
      color: white;
      border-radius: 50%;
      text-align: center;
      line-height: 36px;
      font-weight: 700;
      font-size: 1rem;
      margin-bottom: 12px;
    }}
    .step-do {{
      font-weight: 600;
      font-size: 1.1rem;
      color: #2d2a26;
      margin-bottom: 8px;
    }}
    .step-why {{
      font-size: 0.95rem;
      color: #7a756d;
      line-height: 1.6;
    }}

    .status-card {{
      background: white;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 16px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }}
    .status-label {{ font-size: 0.85rem; color: #7a756d; margin-bottom: 4px; }}
    .status-value {{ font-size: 1.25rem; font-weight: 600; color: #2d2a26; }}
    .signal {{
      display: inline-block;
      padding: 6px 14px;
      border-radius: 20px;
      font-weight: 600;
      font-size: 0.9rem;
    }}
    .signal.LOW {{ background: #d4edda; color: #2d6a3e; }}
    .signal.NEUTRAL {{ background: #fff3cd; color: #856404; }}
    .signal.HIGH {{ background: #f8d7da; color: #721c24; }}

    .picks {{ display: flex; flex-direction: column; gap: 12px; }}
    .pick {{
      background: white;
      border-radius: 12px;
      padding: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      border-left: 4px solid #5c7c6b;
    }}
    .pick-ticker {{ font-weight: 700; font-size: 1.1rem; color: #5c7c6b; }}
    .pick-name {{ color: #2d2a26; }}
    .pick-amt {{ font-weight: 600; color: #7a756d; }}

    .rule {{
      background: white;
      border-radius: 12px;
      padding: 16px 20px;
      margin-bottom: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      display: flex;
      gap: 16px;
      align-items: flex-start;
    }}
    .rule-icon {{ font-size: 1.25rem; }}
    .rule-text {{ flex: 1; }}
    .rule-do {{ font-weight: 600; margin-bottom: 4px; }}
    .rule-why {{ font-size: 0.9rem; color: #7a756d; }}

    .footer {{
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid rgba(0,0,0,0.08);
      font-size: 0.85rem;
      color: #7a756d;
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="logo">LAKSHMI</div>
    <p class="tagline">Your betting guide. One step at a time.</p>

    <div class="section">
      <div class="section-title">Right Now</div>
      <div class="status-card">
        <div class="status-label">Market timing</div>
        <div class="status-value"><span class="signal {signal}">{signal}</span> — {vol_pct}%</div>
        <p style="margin-top:12px;font-size:0.9rem;color:#7a756d;">
          LOW = good time to buy. NEUTRAL = okay. HIGH = wait or bet less.
        </p>
      </div>
    </div>

    <div class="section">
      <div class="section-title">What to buy today</div>
      <div class="picks">{rec_html}
      </div>
      <p style="margin-top:16px;font-size:0.95rem;color:#7a756d;">
        Open Robinhood or Webull. Search each ticker. Buy the amount shown. Use fractional shares.
      </p>
    </div>

    <div class="section">
      <div class="section-title">The steps — do them in order</div>

      <div class="step">
        <div class="step-num">1</div>
        <div class="step-do">Run the system to get your picks.</div>
        <div class="step-why">Open Terminal. Type: python lakshmi_system.py. This tells you what to buy and when.</div>
      </div>

      <div class="step">
        <div class="step-num">2</div>
        <div class="step-do">Check: Do you have an edge?</div>
        <div class="step-why">Edge means the math says you'll win over time. TESS score 85+ = edge. If no edge, don't bet.</div>
      </div>

      <div class="step">
        <div class="step-num">3</div>
        <div class="step-do">Check: Is now a good time?</div>
        <div class="step-why">Look at the market timing above. LOW or NEUTRAL = go ahead. HIGH = wait or bet half.</div>
      </div>

      <div class="step">
        <div class="step-num">4</div>
        <div class="step-do">Decide how much to bet.</div>
        <div class="step-why">Split your budget across your picks. $30 = $10 each for 3 picks. Never bet more than you can lose.</div>
      </div>

      <div class="step">
        <div class="step-num">5</div>
        <div class="step-do">Open your broker and buy.</div>
        <div class="step-why">Robinhood, Webull, or Fidelity. Search the ticker. Buy the exact amount. Done.</div>
      </div>

      <div class="step">
        <div class="step-num">6</div>
        <div class="step-do">Walk away. Don't check every day.</div>
        <div class="step-why">Emotion kills. Revenge betting kills. Hold 6–12 months. Let the edge work.</div>
      </div>

      <div class="step">
        <div class="step-num">7</div>
        <div class="step-do">Repeat tomorrow.</div>
        <div class="step-why">Run the system again. Get new picks. Same steps. The dance never stops.</div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">Rules — never break these</div>

      <div class="rule">
        <span class="rule-icon">✕</span>
        <div class="rule-text">
          <div class="rule-do">Don't bet when you're upset or chasing a loss.</div>
          <div class="rule-why">Emotion makes you bet wrong. Walk away.</div>
        </div>
      </div>
      <div class="rule">
        <span class="rule-icon">✕</span>
        <div class="rule-text">
          <div class="rule-do">Don't bet more than your budget.</div>
          <div class="rule-why">One bad streak can't wipe you out if you size right.</div>
        </div>
      </div>
      <div class="rule">
        <span class="rule-icon">✕</span>
        <div class="rule-text">
          <div class="rule-do">Don't FOMO into something everyone's talking about.</div>
          <div class="rule-why">By the time it's popular, the edge is usually gone.</div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">When you're stuck, ask</div>
      <div class="status-card">
        <p style="font-size:1rem;line-height:1.8;">
          <strong>Why bet?</strong> Because you have an edge. The math says you'll win over time.<br><br>
          <strong>When?</strong> When the system says LOW or NEUTRAL. Not when you feel like it.<br><br>
          <strong>How much?</strong> Your budget divided by your picks. $10 each if you have $30 and 3 picks.<br><br>
          <strong>How little?</strong> Don't bet if you have no edge. Minimum is $0.
        </p>
      </div>
    </div>

    <div class="footer">
      Last updated: {data.get("last_run", "Never")[:19]}<br>
      Run python dashboard/generate_dashboard.py --fresh to update.
    </div>
  </div>
</body>
</html>'''
    return html


def main():
    if "--fresh" in sys.argv:
        run_bot_first()
    data = load_data()
    html = generate_html(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Dashboard written: {OUTPUT}")
    print(f"Open: file://{OUTPUT.absolute()}")


if __name__ == "__main__":
    main()
