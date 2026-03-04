#!/bin/bash
# LAKSHMI — Open Betting Dashboard
cd "$(dirname "$0")"
python3 dashboard/generate_dashboard.py
open dashboard/index.html
