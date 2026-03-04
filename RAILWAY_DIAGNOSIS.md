# Railway Deployment — Root Cause Analysis

## What We Found

### 1. **Start Command Override (most likely)**
Railway docs: *"When you set a custom start command for a Dockerfile deployment, it overrides the Dockerfile CMD and runs in exec form. Exec form does NOT expand variables."*

**If you have a custom Start Command in Railway** → `$PORT` is passed literally → gunicorn gets `'$PORT'` as port → "not a valid port number"

**Fix:** Railway Dashboard → web service → **Settings** → **Deploy** → **Start Command**: **Leave blank** (let Dockerfile CMD run) OR use:
```
/bin/sh -c "exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --timeout 120 app:app"
```

### 2. **PORT Variable**
Railway injects `PORT` at runtime. If using "target ports" or custom networking, you may need to **explicitly set** `PORT=8080` in Railway Variables.

**Fix:** Railway Dashboard → web service → **Variables** → Add `PORT` = `8080`

### 3. **Healthcheck Hostname**
Railway healthchecks come from `healthcheck.railway.app`. If your app restricts by hostname, it would reject them. (Flask/gunicorn do not restrict by default.)

### 4. **Healthcheck Port Mismatch**
"If your application doesn't listen on the PORT variable... health check returns service unavailable."

Our app must listen on whatever port Railway expects. We now hardcode 8080 (Railway's default).

---

## Checklist Before Deploy

- [ ] **Settings → Deploy → Start Command**: Empty (use Dockerfile) or `/bin/sh -c "exec gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 1 --timeout 120 app:app"`
- [ ] **Variables**: Add `PORT` = `8080` if not present
- [ ] **Settings → Health Check**: Path `/api/health` or `/` — or disable to test
