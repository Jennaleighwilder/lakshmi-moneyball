# Deploy LAKSHMI to Vercel

## Push to Git + Deploy

```bash
cd ~/lakshmi-moneyball

# 1. Init git (if not already)
git init

# 2. Add your remote (replace with YOUR repo URL)
git remote add origin https://github.com/YOUR_USERNAME/lakshmi-moneyball.git

# 3. Add, commit, push
git add .
git commit -m "LAKSHMI dashboard - database layout, learn section"
git push -u origin main
```

## Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) → New Project
2. Import your GitHub repo (`lakshmi-moneyball`)
3. Vercel auto-detects Flask (app.py)
4. Deploy

Or with Vercel CLI:

```bash
npm i -g vercel
vercel
```

## Note

On Vercel (serverless), the app runs per-request. No background refresh. First load may take ~15 sec while it runs the scan. Data refreshes when you hit the page or click Refresh.
