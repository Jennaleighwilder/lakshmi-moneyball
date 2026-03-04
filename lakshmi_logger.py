"""
LAKSHMI logger — log everything, store history for learning.
Every scan, every pick, every error gets logged and appended to history.
"""
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from config import LOGS_DIR, HISTORY_FILE, ensure_dirs

ensure_dirs()

LOG_FILE = LOGS_DIR / "lakshmi.log"


def _setup_logger():
    logger = logging.getLogger("lakshmi")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setLevel(logging.INFO)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except OSError:
        pass
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


_logger = _setup_logger()


def log(msg: str, level: str = "info"):
    getattr(_logger, level)(msg)


def log_scan(data: dict):
    """Append scan to history — for learning over time."""
    ensure_dirs()
    entry = {
        "ts": datetime.now().isoformat(),
        "type": "scan",
        "recommendations": data.get("recommendations", []),
        "vol_regime": data.get("vol_regime", {}),
        "live_prices": data.get("live_prices", {}),
    }
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        _logger.warning(f"Failed to append history: {e}")


def log_pick(ticker: str, company: str, confidence: int, amount: float, price: float = None):
    """Log a pick event."""
    _logger.info(f"PICK {ticker} {company} TESS={confidence} amt=${amount} price={price}")


def log_error(msg: str, exc: Exception = None):
    """Log error."""
    _logger.error(msg, exc_info=exc)


def get_history_count() -> int:
    """Count history entries."""
    try:
        if not HISTORY_FILE.exists():
            return 0
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0
