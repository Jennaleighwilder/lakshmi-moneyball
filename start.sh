#!/bin/sh
# Railway sets PORT; default 8080
PORT="${PORT:-8080}"
echo "Starting LAKSHMI on port $PORT"
exec gunicorn --bind "0.0.0.0:$PORT" --workers 1 --timeout 120 app:app
