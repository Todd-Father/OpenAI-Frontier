# OpenAI Frontier Daily Digest - Actual Working Setup Guide

**Date:** February 16, 2026
**Status:** ✅ Tested and Working

This document captures the **exact steps that worked** to set up the automated daily digest, including solutions to common issues.

---

## Overview

This setup creates an automated system that:
- Runs every weekday at 7am EST via GitHub Actions
- Searches for OpenAI Frontier news using NewsAPI
- Ranks and selects top 3-7 stories
- Sends formatted digest via SendGrid to your email
- Saves digest locally as markdown files
- **Total Cost: $0/month** (all free tiers)

---

## Prerequisites

- GitHub account (existing repo: `Todd-Father/OpenAI-Frontier`)
- Gmail account for receiving digests
- **Time required:** 30-45 minutes

---

## Part 1: SendGrid Setup (Email Delivery)

### Step 1.1: Create SendGrid Account

1. Go to [sendgrid.com/pricing](https://sendgrid.com/pricing)
2. Click **"Try for Free"** or **"Sign Up"**
3. Fill in registration:
   - Email: Your email
   - Password: Create strong password
   - Accept terms
4. Verify email address (check inbox and click verification link)
5. Complete onboarding questions (select appropriate options)

### Step 1.2: Verify Sender Email (CRITICAL - Don't Skip!)

**This step is required or you'll get 403 Forbidden errors!**

1. Go to: [app.sendgrid.com/settings/sender_auth/senders](https://app.sendgrid.com/settings/sender_auth/senders)

2. Click **"Create New Sender"** or **"Verify a Single Sender"**

3. Fill in the form:
   - **From Name:** `OpenAI Frontier Digest` (or your preference)
   - **From Email Address:** `tbeavers12@gmail.com` (MUST match the email you'll use)
   - **Reply To:** `tbeavers12@gmail.com` (same as From Email)
   - **Company Address:** Your address (required but not shown in emails)
   - **City, State, ZIP, Country:** Fill in accurately
   - **Nickname:** `Daily Digest Sender` (internal label only)

4. Click **"Create"**

5. **Check your Gmail inbox** (`tbeavers12@gmail.com`)
   - Email subject: "Please Verify Your Sender"
   - Click **"Verify Single Sender"** button in email
   - You'll be redirected to SendGrid confirmation page

6. **Verify success:**
   - Go back to [app.sendgrid.com/settings/sender_auth/senders](https://app.sendgrid.com/settings/sender_auth/senders)
   - You should see `tbeavers12@gmail.com` with a **green checkmark** ✅
   - If no checkmark, email verification didn't work - repeat step 5

### Step 1.3: Create SendGrid API Key

1. Go to: [app.sendgrid.com/settings/api_keys](https://app.sendgrid.com/settings/api_keys)

2. Click **"Create API Key"**

3. Configure:
   - **API Key Name:** `OpenAI-Frontier-Final` (or any descriptive name)
   - **API Key Permissions:** Select **"Full Access"** (top radio button)
     - **IMPORTANT:** Use "Full Access", NOT "Restricted Access"
     - This prevents permission-related 403 errors

4. Click **"Create & View"**

5. **COPY THE ENTIRE API KEY IMMEDIATELY:**
   - Starts with `SG.`
   - About 69 characters long
   - Looks like: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **You can only see this ONCE!**
   - Save it in a secure temporary location (Notes app, password manager)

6. **IMPORTANT:** Keep this window open or save the key - you'll need it in Part 3

**⚠️ Common Issue:** If you create multiple API keys, delete the old ones to avoid confusion. Only keep one active key.

---

## Part 2: NewsAPI Setup (News Gathering)

### Step 2.1: Create NewsAPI Account

1. Go to: [newsapi.org/register](https://newsapi.org/register)

2. Fill in registration:
   - First Name, Last Name
   - Email address
   - Password
   - Select "I'm using this for: Personal Project" (free tier)

3. Click **"Submit"**

4. Verify email (check inbox and click verification link)

### Step 2.2: Get API Key

1. After login, you're automatically shown your dashboard

2. **Your API key is displayed prominently** at the top:
   - 32-character alphanumeric string
   - Looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **Copy the entire key** and save temporarily

**Free Tier Limits:**
- 100 requests per day (perfect for 1 daily digest)
- Access to news from past 30 days

---

## Part 3: GitHub Repository & Secrets Configuration

### Step 3.1: Push Code to GitHub

**Note:** This was already done, but here's the process for reference:

```bash
cd "/Users/toddbeavers/OpenAI Frontier"
git init
git add .
git commit -m "Initial commit: Daily digest automation"
git remote add origin https://github.com/Todd-Father/OpenAI-Frontier.git
git push -u origin main
```

If you get authentication errors:
- Create Personal Access Token: [github.com/settings/tokens/new](https://github.com/settings/tokens/new)
- Scopes needed: `repo` ✅ and `workflow` ✅
- Use token as password when pushing

### Step 3.2: Configure GitHub Secrets (CRITICAL STEP)

**This is where most issues occur - follow exactly!**

1. Go to: [github.com/Todd-Father/OpenAI-Frontier/settings/secrets/actions](https://github.com/Todd-Father/OpenAI-Frontier/settings/secrets/actions)

2. **Add Secret #1: SENDGRID_API_KEY**
   - Click **"New repository secret"**
   - Name: `SENDGRID_API_KEY` (exactly, case-sensitive)
   - Secret: Paste your SendGrid API key (from Part 1.3, starts with `SG.`)
   - Click **"Add secret"**

3. **Add Secret #2: RECIPIENT_EMAIL**
   - Click **"New repository secret"**
   - Name: `RECIPIENT_EMAIL` (exactly, case-sensitive)
   - Secret: `tbeavers12@gmail.com`
   - Click **"Add secret"**

4. **Add Secret #3: NEWSAPI_KEY**
   - Click **"New repository secret"**
   - Name: `NEWSAPI_KEY` (exactly, case-sensitive)
   - Secret: Paste your NewsAPI key (from Part 2.2, 32 characters)
   - Click **"Add secret"**

5. **Add Secret #4: SENDER_EMAIL (CRITICAL!)**
   - Click **"New repository secret"**
   - Name: `SENDER_EMAIL` (exactly, case-sensitive)
   - Secret: `tbeavers12@gmail.com` (MUST match verified email from Part 1.2)
   - Click **"Add secret"**

**Verify All 4 Secrets Are Present:**

You should now see exactly these 4 secrets listed:
- ✅ `NEWSAPI_KEY`
- ✅ `RECIPIENT_EMAIL`
- ✅ `SENDER_EMAIL` ← Don't skip this one!
- ✅ `SENDGRID_API_KEY`

**⚠️ Common Mistake:** Forgetting to add `SENDER_EMAIL` causes 403 Forbidden errors!

---

## Part 4: Test the Digest

### Step 4.1: Manual Workflow Trigger

1. Go to: [github.com/Todd-Father/OpenAI-Frontier/actions](https://github.com/Todd-Father/OpenAI-Frontier/actions)

2. In left sidebar, click **"Daily OpenAI Frontier Digest"**

3. On the right side, click **"Run workflow"** dropdown button

4. Click the green **"Run workflow"** button

5. Wait 10-20 seconds, then **refresh the page**

6. You should see a new workflow run appear (yellow circle = running, green check = completed)

### Step 4.2: Check Workflow Logs

1. Click on the workflow run (should show green checkmark after ~30 seconds)

2. Click on **"generate-digest"** job (left side)

3. Expand **"Generate and send digest"** step

4. **Look for these SUCCESS indicators:**
   ```
   ============================================================
   OpenAI Frontier Daily Digest Generator
   ============================================================

   Date: 2026-02-16 XX:XX

   Searching for OpenAI Frontier news...
   Found 3 articles
   Analyzing and ranking 3 articles...
   Generating digest for 2 stories...
   Saving digest locally...
   Digest saved to: daily-digests/2026-02-16.md
   Sending email to ***...
   Email sent successfully! Status code: 202  ← THIS IS SUCCESS!

   ============================================================
   SUMMARY
   ============================================================
   Stories found: 3
   Stories selected: 2
   Digest saved: Yes
   Email sent: Yes  ← THIS SHOULD SAY "Yes"

   ✅ Digest successfully sent to ***
   ============================================================
   ```

5. **If you see this instead (FAILURE):**
   ```
   Error sending email: HTTP Error 403: Forbidden
   Email sent: No
   ```

   **Go to Part 5: Troubleshooting below!**

### Step 4.3: Check Your Email

1. Open Gmail: [mail.google.com](https://mail.google.com)

2. Log in to `tbeavers12@gmail.com`

3. Check inbox for email with:
   - **Subject:** "OpenAI Frontier Daily Digest - [Today's Date]"
   - **From:** OpenAI Frontier Digest (or tbeavers12@gmail.com)
   - **Content:** 2-7 news stories with summaries

4. **If not in inbox:**
   - Check **Spam folder**
   - If found in spam, mark as "Not Spam"
   - Add sender to contacts to prevent future spam filtering

---

## Part 5: Troubleshooting Common Issues

### Issue 1: "Error sending email: HTTP Error 403: Forbidden"

**Cause:** One of these is wrong:
- Sender email not verified in SendGrid
- SENDER_EMAIL secret missing or incorrect
- API key has wrong permissions

**Solution:**

1. **Verify sender email has green checkmark:**
   - Go to: [app.sendgrid.com/settings/sender_auth/senders](https://app.sendgrid.com/settings/sender_auth/senders)
   - Must show `tbeavers12@gmail.com` with ✅
   - If no checkmark: Repeat Part 1.2

2. **Verify SENDER_EMAIL secret exists:**
   - Go to: [github.com/Todd-Father/OpenAI-Frontier/settings/secrets/actions](https://github.com/Todd-Father/OpenAI-Frontier/settings/secrets/actions)
   - Must show `SENDER_EMAIL` in the list
   - If missing: Add it (Part 3.2, step 5)

3. **Check SENDER_EMAIL appears in workflow debug output:**
   - Go to Actions → Latest run → generate-digest job
   - Look for this line in debug section:
     ```
     ##[debug]Evaluating: secrets.SENDER_EMAIL
     ```
   - If missing: The workflow file is outdated, you need to pull latest code

4. **Create fresh API key with Full Access:**
   - Go to: [app.sendgrid.com/settings/api_keys](https://app.sendgrid.com/settings/api_keys)
   - Delete all existing keys
   - Create ONE new key with **"Full Access"** (not Restricted)
   - Update `SENDGRID_API_KEY` secret with new key

5. **Test again** (Part 4.1)

### Issue 2: "No files were found with the provided path: daily-digests/*.md"

**Status:** This is a **WARNING, not an error** - it's expected!

**Explanation:** The `daily-digests/` folder is gitignored and only exists locally or as GitHub Actions artifacts. This warning is harmless and does not affect email delivery.

### Issue 3: Email Not Received (No Errors in Logs)

**Checklist:**

1. **Check SendGrid Activity:**
   - Go to: [app.sendgrid.com/email_activity](https://app.sendgrid.com/email_activity)
   - Should show "REQUESTS: 1" and "DELIVERED: 1"
   - If 0 requests: Email was never sent, check logs for errors

2. **Check Gmail Spam folder**

3. **Check workflow says "Email sent: Yes"** in summary

4. **Wait a few minutes** - sometimes delivery is delayed

### Issue 4: "WARNING: Only found 2 relevant articles (minimum is 3)"

**Status:** This is a **WARNING, not an error**

**Cause:** Not enough high-quality OpenAI Frontier news in past 24-48 hours

**Solution:**
- The digest will still send with 2 stories
- To always get 3-7 stories, edit `scripts/config.py`:
  ```python
  MIN_STORIES = 2  # Lower minimum
  ```
- Or add more search queries in `config.py`

### Issue 5: Workflow File Doesn't Have SENDER_EMAIL

**Check:**
1. Go to: [github.com/Todd-Father/OpenAI-Frontier/blob/main/.github/workflows/daily-digest.yml](https://github.com/Todd-Father/OpenAI-Frontier/blob/main/.github/workflows/daily-digest.yml)
2. Look at line 36 - should show:
   ```yaml
   SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}
   ```

**If missing:**
- Pull latest code from the repository
- Or manually add the line to the workflow file and commit

---

## Part 6: Verify Automated Schedule

### Understanding the Schedule

The digest runs automatically via GitHub Actions cron:

```yaml
cron: '0 12 * * 1-5'
```

**Breakdown:**
- `0 12` = 12:00 UTC
- `* *` = Every day of month, every month
- `1-5` = Monday through Friday (1=Mon, 5=Fri)

**Timezone Conversion:**
- **Winter (EST):** 12:00 UTC = 7:00 AM EST ✅
- **Summer (EDT):** 12:00 UTC = 8:00 AM EDT ⚠️

**To receive at 7am year-round:**
- Winter: Use `'0 12 * * 1-5'` (current setting)
- Summer: Change to `'0 11 * * 1-5'` in March
- Change back in November

**Or:** Accept 8am delivery during daylight saving time

### First Scheduled Run

**When:** Next weekday (Monday-Friday) at 7:00 AM EST

**How to verify:**
1. Wake up Monday-Friday after 7am
2. Check email: tbeavers12@gmail.com
3. Should have digest with subject: "OpenAI Frontier Daily Digest - [Date]"
4. Check: [github.com/Todd-Father/OpenAI-Frontier/actions](https://github.com/Todd-Father/OpenAI-Frontier/actions)
   - Should show automatic runs at ~7am EST each weekday

---

## Part 7: Customization (Optional)

### Change Digest Delivery Time

Edit `.github/workflows/daily-digest.yml` line 9:

```yaml
# Current: 7am EST / 8am EDT
- cron: '0 12 * * 1-5'

# For 8am EST / 9am EDT:
- cron: '0 13 * * 1-5'

# For 6am EST / 7am EDT:
- cron: '0 11 * * 1-5'
```

Use [crontab.guru](https://crontab.guru) to calculate UTC times.

### Change Number of Stories

Edit `scripts/config.py` lines 40-41:

```python
MIN_STORIES = 3  # Change to 2 or 5
MAX_STORIES = 7  # Change to 10 for more stories
```

### Add More Search Queries

Edit `scripts/config.py` lines 14-20:

```python
SEARCH_QUERIES = [
    'OpenAI Frontier news',
    'OpenAI Frontier enterprise',
    'OpenAI Frontier security',
    'OpenAI Frontier updates',
    'OpenAI Frontier partnership',
    'OpenAI AI agents',  # Add your own
    'OpenAI enterprise platform',  # Add more
]
```

### Send to Multiple Email Addresses

Edit GitHub Secret `RECIPIENT_EMAIL`:

```
email1@example.com,email2@example.com,email3@example.com
```

(Comma-separated, no spaces)

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│ GitHub Actions (Free Tier)                              │
│ Cron: 7am EST Monday-Friday                             │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ Python Script (generate_digest.py)                      │
│ 1. Search NewsAPI for OpenAI Frontier articles          │
│ 2. Rank by relevance, recency, source authority         │
│ 3. Select top 3-7 stories                                │
│ 4. Generate markdown digest                              │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│ Save Locally     │  │ Send via         │
│ daily-digests/   │  │ SendGrid API     │
│ 2026-02-16.md    │  │                  │
└──────────────────┘  └────────┬─────────┘
                               ▼
                      ┌──────────────────┐
                      │ Your Gmail       │
                      │ tbeavers12@      │
                      │ gmail.com        │
                      └──────────────────┘
```

---

## Success Checklist

Before considering setup complete:

- [x] SendGrid account created
- [x] Sender email verified (green checkmark in SendGrid)
- [x] SendGrid API key created with Full Access
- [x] NewsAPI account created
- [x] All 4 GitHub Secrets configured:
  - [x] SENDGRID_API_KEY
  - [x] RECIPIENT_EMAIL
  - [x] NEWSAPI_KEY
  - [x] SENDER_EMAIL
- [x] Manual workflow test successful
- [x] Email received with "Status code: 202"
- [x] Workflow shows "Email sent: Yes"
- [ ] First scheduled run verified (wait until next weekday 7am)

---

## Key Lessons Learned

### What Caused the Most Issues:

1. **Missing SENDER_EMAIL secret** - Took longest to debug
   - Sender must be verified in SendGrid
   - Secret must be added to GitHub
   - Workflow file must pass it to script

2. **API Key Permissions** - Used Restricted instead of Full Access initially
   - Solution: Always use "Full Access" for simplicity

3. **Multiple API Keys** - Created confusion about which was active
   - Solution: Delete old keys, keep only one

4. **Old Workflow Runs** - Looking at logs from before fixes were applied
   - Solution: Always trigger fresh run after changes

### What Worked Immediately:

- NewsAPI setup (straightforward)
- Local git repository setup
- GitHub Actions workflow syntax
- Python script logic

---

## Maintenance

### Weekly
- [x] Verify emails arriving Monday-Friday at 7am
- [x] Check story quality and relevance

### Monthly
- [ ] Review GitHub Actions usage (should be ~110 min/month)
- [ ] Check SendGrid usage (should be ~22 emails/month)
- [ ] Rotate SendGrid API key (security best practice)
- [ ] Update thought leaders list (see AI-Security-Thought-Leaders.md)

### As Needed
- [ ] Adjust search queries if stories become less relevant
- [ ] Update timezone settings for daylight saving time
- [ ] Review and fill out security questionnaires

---

## Cost Breakdown

| Service | Tier | Usage | Cost |
|---------|------|-------|------|
| GitHub Actions | Free | ~110 min/month | $0 |
| SendGrid | Free | ~22 emails/month | $0 |
| NewsAPI | Free | ~22 requests/month | $0 |
| **Total** | | | **$0/month** |

**Free Tier Limits:**
- GitHub Actions: 2,000 min/month
- SendGrid: 100 emails/day
- NewsAPI: 100 requests/day

---

## Resources

### Documentation
- **This Repo:** [github.com/Todd-Father/OpenAI-Frontier](https://github.com/Todd-Father/OpenAI-Frontier)
- **SendGrid Docs:** [docs.sendgrid.com](https://docs.sendgrid.com)
- **NewsAPI Docs:** [newsapi.org/docs](https://newsapi.org/docs)
- **GitHub Actions Docs:** [docs.github.com/en/actions](https://docs.github.com/en/actions)

### Quick Links
- **GitHub Actions:** [github.com/Todd-Father/OpenAI-Frontier/actions](https://github.com/Todd-Father/OpenAI-Frontier/actions)
- **GitHub Secrets:** [github.com/Todd-Father/OpenAI-Frontier/settings/secrets/actions](https://github.com/Todd-Father/OpenAI-Frontier/settings/secrets/actions)
- **SendGrid Dashboard:** [app.sendgrid.com](https://app.sendgrid.com)
- **SendGrid API Keys:** [app.sendgrid.com/settings/api_keys](https://app.sendgrid.com/settings/api_keys)
- **SendGrid Sender Auth:** [app.sendgrid.com/settings/sender_auth/senders](https://app.sendgrid.com/settings/sender_auth/senders)
- **SendGrid Activity:** [app.sendgrid.com/email_activity](https://app.sendgrid.com/email_activity)
- **NewsAPI Dashboard:** [newsapi.org/account](https://newsapi.org/account)
- **Cron Helper:** [crontab.guru](https://crontab.guru)

---

## Timeline (Actual)

**Total Setup Time: ~45 minutes** (including troubleshooting)

- SendGrid setup: 10 minutes
- NewsAPI setup: 5 minutes
- GitHub secrets configuration: 5 minutes
- Initial testing: 5 minutes
- Troubleshooting 403 errors: 20 minutes
  - Missing SENDER_EMAIL secret
  - API key permissions
  - Multiple API keys confusion
  - Looking at old workflow runs

**If following this guide exactly: ~25 minutes** (without troubleshooting)

---

**Document Version:** 1.0
**Last Updated:** February 16, 2026
**Tested By:** Todd Beavers
**Status:** ✅ Working in Production
