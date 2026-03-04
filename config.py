"""
LAKSHMI config — data dir for logs, state, history.
On Railway: set RAILWAY_VOLUME_MOUNT_PATH and mount a volume to /data
Locally: uses ./data
"""
import os
from pathlib import Path

BOT_DIR = Path(__file__).parent.resolve()
# Railway volume or local data dir
DATA_DIR = Path(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", str(BOT_DIR / "data")))
LOGS_DIR = DATA_DIR / "logs"
STATE_DIR = DATA_DIR / "state"
HISTORY_FILE = DATA_DIR / "history.jsonl"  # append-only, one JSON object per line
DOMAIN_HISTORY_FILE = DATA_DIR / "domain_history.jsonl"  # all 12 domains, for learning

def ensure_dirs():
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        STATE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass  # Read-only fs (e.g. some Railway setups)
