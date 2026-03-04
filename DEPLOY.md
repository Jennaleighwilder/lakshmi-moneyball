# Deploy LAKSHMI to Railway

Railway runs the app 24/7, logs everything, and stores history so it can learn.

## 1. Push to GitHub

```bash
cd ~/lakshmi-moneyball
git add .
git commit -m "Railway: logging, history, persistent storage"
git push origin main
```

## 2. Deploy on Railway

1. Go to [railway.app](https://railway.app) → New Project
2. **Deploy from GitHub** → select your `lakshmi-moneyball` repo
3. Railway auto-detects Python + Procfile

## 3. Add a Volume (for logs + history)

Railway's filesystem is ephemeral by default. To persist logs and history:

1. In your Railway project → **Settings** → **Volumes**
2. Add a volume, mount path: `/data`
3. Railway sets `RAILWAY_VOLUME_MOUNT_PATH=/data` automatically

Your app stores in `/data`:
- `logs/lakshmi.log` — every scan, every error
- `state/chimera_state.json` — Chimera state
- `history.jsonl` — every scan (append-only, for learning)
- `portfolio.json` — current picks

## 4. Generate Domain

Settings → Networking → **Generate Domain** → get your public URL.

## 5. Deploy via CLI (optional)

```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

## What gets logged and stored

- **Every scan** → appended to `history.jsonl` (picks, vol regime, prices)
- **Every scan** → appended to `logs/lakshmi.log`
- **Chimera state** → saved to `state/chimera_state.json` after each analysis
- **Portfolio** → `portfolio.json` updated each scan

Over time, the history grows and Chimera can learn from it.
