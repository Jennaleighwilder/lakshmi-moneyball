#!/usr/bin/env python3
"""Start gunicorn with PORT from environment. Railway sets PORT at runtime."""
import os
import subprocess
import sys

port = os.environ.get("PORT", "8080")
try:
    port = str(int(port))
except (ValueError, TypeError):
    port = "8080"

print(f"Starting LAKSHMI on port {port}", flush=True)
sys.exit(
    subprocess.call(
        [
            "gunicorn",
            "--bind", f"0.0.0.0:{port}",
            "--workers", "1",
            "--timeout", "120",
            "app:app",
        ]
    )
)
