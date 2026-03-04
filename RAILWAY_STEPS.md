# How to Fix LAKSHMI on Railway — Step by Step

**Direct link:** After logging in, go to:  
`https://railway.app/project/YOUR_PROJECT_ID/service/YOUR_SERVICE_ID`  
(You can get this from your browser when you're viewing the web service.)

---

## Step 1: Open your project
1. Go to **https://railway.app**
2. Log in
3. Click your project (**imaginative-upliftment**)
4. Click the **web** service (the card with `web-production-ab17a0.up.railway.app`)

---

## Step 2: Clear the Start Command
1. Click **Settings** (or the gear icon)
2. Scroll to **Deploy** section
3. Find **"Start Command"** or **"Custom Start Command"**
4. If there is anything in that box, **delete it** (make it empty)
5. Click **Save** if there's a save button

---

## Step 3: Add PORT variable
1. Click **Variables** (in the left sidebar or tabs)
2. Click **+ New Variable** or **Add Variable**
3. Name: `PORT`
4. Value: `8080`
5. Save

---

## Step 4: Redeploy
1. Go to **Deployments**
2. Click the **⋮** (three dots) on the latest deployment
3. Click **Redeploy**
   
   — OR —
   
   Push any change to GitHub and Railway will auto-deploy

---

## Step 5: Wait and test
1. Wait 1–2 minutes for the build
2. Click your app URL: **web-production-ab17a0.up.railway.app**
3. You should see the LAKSHMI dashboard

---

## If you can't find something

**"I don't see Start Command"**  
→ Look under Settings → Deploy. It might be called "Override" or "Start Command Override."

**"I don't see Variables"**  
→ It's usually a tab next to Deployments, or under Settings.

**"It still doesn't work"**  
→ In Railway, go to your web service → **Deploy Logs** (not Build Logs). Copy the last 20 lines and share them. That will show the real error.
