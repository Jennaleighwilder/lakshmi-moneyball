"""
Domain 6: CRYPTO — Spot via Yahoo, UVRK applies
"""

from typing import List, Dict, Any

CRYPTO_TICKERS = ["BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD"]


def fetch_crypto() -> List[Dict[str, Any]]:
    try:
        import yfinance as yf
        out = []
        for t in CRYPTO_TICKERS:
            try:
                data = yf.download(t, period="5d", progress=False, threads=False)
                if data is not None and len(data) > 0:
                    close_ser = data["Close"].iloc[-1] if "Close" in data.columns else data.iloc[-1]
                    close = float(close_ser.iloc[0]) if hasattr(close_ser, "iloc") else float(close_ser)
                    out.append({
                        "ticker": t,
                        "price": close,
                        "source": "yfinance",
                    })
            except Exception:
                pass
        return out
    except Exception:
        return []
