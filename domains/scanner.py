"""
MULTI-DOMAIN SCANNER — Runs all 12 domains, stores for learning.
Constantly updates. Model learns from all. Eventually branches.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Import domain fetchers
from .prediction import fetch_prediction_markets
from .stocks import fetch_stocks
from .crypto import fetch_crypto


def _fetch_domain(name: str) -> List[Dict]:
    """Fetch one domain. Stubs return [] until implemented."""
    if name == "prediction":
        return fetch_prediction_markets()
    if name == "stocks":
        return fetch_stocks()
    if name == "crypto":
        return fetch_crypto()
    # Stubs: sports, dfs, esports, insurance, casino, horses, sweeps, derivatives, unusual
    return []


def scan_all() -> Dict[str, Any]:
    """Scan all 12 domains. Return combined data for learning."""
    from . import DOMAINS

    results = {}
    for domain in DOMAINS:
        try:
            data = _fetch_domain(domain)
            results[domain] = {
                "count": len(data),
                "items": data[:20],  # cap per domain
                "ts": datetime.now().isoformat(),
            }
        except Exception as e:
            results[domain] = {"count": 0, "items": [], "error": str(e), "ts": datetime.now().isoformat()}

    return {
        "scan_ts": datetime.now().isoformat(),
        "domains": results,
        "total_opportunities": sum(r["count"] for r in results.values()),
    }


def append_to_domain_history(scan_result: Dict, history_path: Path) -> int:
    """Append scan to history — one JSON per line. Model learns from this."""
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with open(history_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(scan_result) + "\n")
    with open(history_path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)
