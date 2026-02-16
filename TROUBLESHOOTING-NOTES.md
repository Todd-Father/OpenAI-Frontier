# Troubleshooting Notes

## Repository Changed to Private - February 16, 2026

**Change Made:** Repository `Todd-Father/OpenAI-Frontier` changed from public to private

**Potential Impact:** GitHub Actions scheduled workflow (7am EST daily digest)

**What to Check if Tomorrow's Digest Fails (February 17, 2026):**

### 1. Verify GitHub Actions is Enabled

Go to: [github.com/Todd-Father/OpenAI-Frontier/settings/actions](https://github.com/Todd-Father/OpenAI-Frontier/settings/actions)

**Check:**
- [ ] "Allow all actions and reusable workflows" is selected
- [ ] If disabled, enable it and re-run workflow

### 2. Check Workflow Permissions

Still in Settings → Actions:

**Scroll to "Workflow permissions" section:**
- [ ] "Read and write permissions" should be selected
- [ ] If "Read repository contents and packages permissions" is selected instead, change it

### 3. Check GitHub Actions Logs

Go to: [github.com/Todd-Father/OpenAI-Frontier/actions](https://github.com/Todd-Father/OpenAI-Frontier/actions)

**Look for:**
- Yellow circle (running) or red X (failed) around 7:00-7:05 AM EST
- Click on the run to see error message
- Common errors for private repos:
  - "Actions is disabled for this repository"
  - "Resource not accessible by integration"
  - Permission errors

### 4. Quick Fix Steps

**If workflow failed due to permissions:**

```bash
# Re-enable Actions and set permissions
1. Go to Settings → Actions → General
2. Enable: "Allow all actions and reusable workflows"
3. Under "Workflow permissions": Select "Read and write permissions"
4. Click "Save"
5. Go to Actions tab → Daily OpenAI Frontier Digest → Run workflow
```

### 5. Verify Free Tier Limits

**GitHub Free tier for private repos:**
- ✅ 2,000 minutes/month (we use ~110 minutes/month)
- ✅ Should be no issue with limits

**If you see usage warnings:**
- Go to Settings → Billing and plans
- Check Actions minutes usage

---

## Recent Bug Fixes

### February 16, 2026 - Fixed AttributeError on None Values

**Error:**
```
AttributeError: 'NoneType' object has no attribute 'lower'
```

**Cause:** NewsAPI sometimes returns `None` for description/title/content fields

**Fix:** Updated code to use `or ''` pattern:
```python
# Before:
description = story.get('description', '').lower()

# After:
description = (story.get('description') or '').lower()
```

**Status:** ✅ Fixed and deployed (commit: b3e772f)

---

## Working Configuration (As of February 16, 2026)

### GitHub Secrets (All 4 Required):
- ✅ `SENDGRID_API_KEY` - Full Access key
- ✅ `RECIPIENT_EMAIL` - tbeavers12@gmail.com
- ✅ `NEWSAPI_KEY` - NewsAPI key
- ✅ `SENDER_EMAIL` - tbeavers12@gmail.com (verified in SendGrid)

### SendGrid Configuration:
- ✅ Sender verified: tbeavers12@gmail.com with green checkmark
- ✅ API Key: OpenAI-Frontier-Final (Full Access)
- ✅ Free tier: 100 emails/day

### NewsAPI Configuration:
- ✅ Account active
- ✅ Free tier: 100 requests/day

### Last Successful Manual Test:
- **Date:** February 16, 2026 ~2:30 AM EST
- **Status:** ✅ Email sent successfully (Status code: 202)
- **Stories:** 2 stories found and sent
- **Email received:** Confirmed in tbeavers12@gmail.com

### Next Scheduled Run:
- **Date:** Monday, February 17, 2026
- **Time:** 7:00 AM EST (12:00 UTC)
- **Cron:** `'0 12 * * 1-5'`

---

## If You See These Errors Tomorrow:

### "Actions is disabled for this repository"
→ Enable Actions in Settings → Actions → General

### "Resource not accessible by integration"
→ Set "Read and write permissions" in Workflow permissions

### "HTTP Error 403: Forbidden" (email sending)
→ SendGrid issue, not related to private repo change
→ See SETUP-ACTUAL-WORKING-STEPS.md Issue #1

### "AttributeError: 'NoneType' object has no attribute 'lower'"
→ Already fixed! If you see this, code wasn't updated
→ Pull latest code: `git pull origin main`

### No error, but no email received
→ Check SendGrid activity: [app.sendgrid.com/email_activity](https://app.sendgrid.com/email_activity)
→ Should show REQUESTS: 1, DELIVERED: 1

---

## Quick Health Check Commands

Run these if you need to verify everything:

```bash
# 1. Check current branch and status
cd "/Users/toddbeavers/OpenAI Frontier"
git status
git log --oneline -5

# 2. Verify workflow file has SENDER_EMAIL
grep -A 2 "SENDER_EMAIL" .github/workflows/daily-digest.yml

# 3. Test locally (optional - requires .env file)
cd scripts
python generate_digest.py
```

---

**Last Updated:** February 16, 2026
**Next Review:** February 17, 2026 (after first scheduled run with private repo)
