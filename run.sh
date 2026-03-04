#!/bin/bash
# LAKSHMI — Run locally or on Railway
cd "$(dirname "$0")"
source .venv/bin/activate 2>/dev/null || true
export PORT="${PORT:-5001}"
echo "LAKSHMI starting on port $PORT"
echo "Open: http://127.0.0.1:$PORT"
exec gunicorn --bind "0.0.0.0:$PORT" --workers 1 --timeout 120 app:app
