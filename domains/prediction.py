"""
Domain 1: PREDICTION MARKETS — Kalshi + Polymarket
Free APIs, no auth. Binary outcomes, implied probability.
"""

import json
import urllib.request
from typing import List, Dict, Any

from .base import DomainFetcher


class PolymarketFetcher(DomainFetcher):
    domain = "polymarket"

    def fetch(self) -> List[Dict[str, Any]]:
        try:
            req = urllib.request.Request(
                "https://gamma-api.polymarket.com/events?active=true&closed=false&limit=20",
                headers={"User-Agent": "LAKSHMI/1.0"},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                events = json.loads(r.read().decode())
        except Exception:
            return []
        out = []
        for ev in events[:10]:
            markets = ev.get("markets", [])
            for m in markets[:1]:
                prices = m.get("outcomePrices", ["0.5", "0.5"])
                yes_price = float(prices[0]) if prices else 0.5
                out.append({
                    "ticker": ev.get("slug", "")[:20],
                    "title": ev.get("title", "")[:80],
                    "yes_price": yes_price,
                    "no_price": 1 - yes_price,
                    "category": ev.get("category", ""),
                    "source": "polymarket",
                })
        return out


class KalshiFetcher(DomainFetcher):
    domain = "kalshi"

    def fetch(self) -> List[Dict[str, Any]]:
        try:
            req = urllib.request.Request(
                "https://api.elections.kalshi.com/trade-api/v2/events?status=open&limit=15",
                headers={"User-Agent": "LAKSHMI/1.0"},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
        except Exception:
            return []
        events = data.get("events", [])
        out = []
        for ev in events[:10]:
            out.append({
                "ticker": ev.get("event_ticker", ""),
                "title": ev.get("title", "")[:80],
                "category": ev.get("category", ""),
                "source": "kalshi",
            })
        return out


def fetch_prediction_markets() -> List[Dict]:
    """Fetch from Polymarket + Kalshi."""
    out = []
    for fetcher in [PolymarketFetcher(), KalshiFetcher()]:
        try:
            out.extend(fetcher.fetch())
        except Exception:
            pass
    return out
