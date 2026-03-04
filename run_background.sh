#!/bin/bash
# LAKSHMI Moneyball — Run in background
# Add to crontab: 0 9 * * * /Users/jenniferwest/lakshmi-moneyball/run_background.sh

cd /Users/jenniferwest/lakshmi-moneyball
mkdir -p logs
python3 lakshmi_bot.py --background >> logs/bot.log 2>&1
