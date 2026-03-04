# LAKSHMI — Make It Work

## Run locally (instant)

```bash
cd ~/lakshmi-moneyball
source .venv/bin/activate
./run.sh
```

Then open: **http://127.0.0.1:5001** (or the port shown)

## Deploy to Railway

1. Push to GitHub
2. Railway auto-deploys from the repo
3. Open your Railway URL

## What was fixed

- **Quick load**: `/api/quick` returns in ~30ms with no Yahoo/Chimera/domains. Page shows immediately.
- **Background full load**: `/api/data` runs in background; live prices and domains update when ready.
- **Timeouts**: Yahoo Finance 8s max, Chimera 5s max — never hangs.
- **Retry button**: If connection fails, click Retry instead of auto-retry loop.

## If it still doesn't work

1. **Locally**: Run `python -c "from app import app; print('OK')"` — if that fails, fix the import.
2. **Railway**: Check logs for errors. Ensure PORT is set (Railway does this automatically).
3. **Browser**: Open DevTools → Network. See if `/api/quick` returns 200.
