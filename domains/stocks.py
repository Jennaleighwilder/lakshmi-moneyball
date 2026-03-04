"""
Domain 5: STOCKS — TESS + Yahoo (existing lakshmi_bot)
"""

from typing import List, Dict, Any


def fetch_stocks() -> List[Dict[str, Any]]:
    """Uses existing TESS + UVRK scan. Returns recommendations."""
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from config import DATA_DIR
        import json
        pf = DATA_DIR / "portfolio.json"
        if pf.exists():
            with open(pf) as f:
                data = json.load(f)
            recs = data.get("recommendations", [])
            return [{"ticker": r["ticker"], "company": r["company"], "confidence": r["confidence"], "amount": r.get("amount", 10), "sector": r.get("sector", ""), "source": "tess"} for r in recs]
    except Exception:
        pass
    return []
