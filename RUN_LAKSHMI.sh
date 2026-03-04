#!/bin/bash
# LAKSHMI — Run the live dashboard
# Real data. Chimera learns. She explains.
# Run in foreground by default. Use --background to daemonize.

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "First run: creating virtual environment..."
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -q flask yfinance pandas
else
  source .venv/bin/activate
fi

if [ "$1" = "--background" ] || [ "$1" = "-b" ]; then
  echo "LAKSHMI — Starting in background..."
  nohup python lakshmi_app.py >> logs/lakshmi.log 2>&1 &
  PID=$!
  mkdir -p logs
  echo $PID > logs/lakshmi.pid
  echo "Started. PID: $PID"
  echo "Log: tail -f logs/lakshmi.log"
  echo "Stop: kill \$(cat logs/lakshmi.pid)"
  echo "Open: http://127.0.0.1:5001"
  exit 0
fi

echo ""
echo "LAKSHMI — Live Dashboard"
echo "================================"
echo "Open: http://127.0.0.1:5001"
echo "Real data · Chimera learning"
echo "================================"
echo ""

python lakshmi_app.py
