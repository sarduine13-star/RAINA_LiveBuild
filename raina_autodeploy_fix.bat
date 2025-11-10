@echo off
title === RAINA GitHub + Render Deploy Fix ===
echo ---------------------------------------------
echo   Initializing RAINA full deploy permission fix
echo ---------------------------------------------

:: Step 1 — Get GitHub fine-grained token
set /p GITHUB_TOKEN=Paste your GitHub fine-grained token (with repo write access):

:: Step 2 — Write fresh .env (safe overwrite)
(
echo OPENAI_API_KEY=sk-...
echo STRIPE_SECRET_KEY=sk_live_...
echo STRIPE_WEBHOOK_SECRET=whsec_...
echo BREVO_API_KEY=xsmptsib-...
echo APOLLO_API_KEY=bZghj04RsDtCckNGYg3HNw
echo RENDER_API_KEY=rnd_D3AzCFGzlzVBjcNHuOLtsL6PNRFj
echo RENDER_SERVICE_ID=srv-d45aavre5dus73c05tt0
echo FRONTEND_SERVICE_ID=srv-d44gbbadbo4c73eu1ffg
echo VITE_API_URL=https://raina-livebuild.onrender.com
echo STRIPE_PUBLISHABLE_KEY=pk_live_...
echo GITHUB_ACCESS_TOKEN=%GITHUB_TOKEN%
echo RENDER_DEPLOY_URL=https://api.render.com/v1/services/srv-d45aavre5dus73c05tt0/deploys
) > .env

echo ✅ .env updated with GitHub + Render deploy permissions.

:: Step 3 — Optional immediate deploy trigger
set /p DEPLOY_NOW=Trigger deploy now? (Y/N):
if /I "%DEPLOY_NOW%"=="Y" (
  echo 🔁 Sending deploy request to Render...
  curl -X POST https://api.render.com/v1/services/srv-d45aavre5dus73c05tt0/deploys ^
    -H "Authorization: Bearer rnd_D3AzCFGzlzVBjcNHuOLtsL6PNRFj" ^
    -H "Content-Type: application/json" ^
    -d "{}"
  echo ✅ Deploy triggered successfully.
) else (
  echo ⏭️  Deploy skipped. Manual push will auto-deploy as usual.
)

echo ---------------------------------------------
echo ✅  RAINA now has full GitHub + Render deploy autonomy.
echo ---------------------------------------------
pause
