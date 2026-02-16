# Setup Guide: OpenAI Frontier Daily Digest

This guide will walk you through setting up the automated daily digest system that runs every weekday at 7am and emails you the top OpenAI Frontier news stories.

**Estimated Setup Time:** 20-30 minutes

---

## Prerequisites

Before you begin, make sure you have:

- ✅ A GitHub account (free tier is fine)
- ✅ A SendGrid account (free tier: 100 emails/day)
- ✅ A NewsAPI account (free tier: 100 requests/day) - *optional but recommended*
- ✅ Git installed on your computer
- ✅ Python 3.11+ installed (for local testing only)

---

## Step 1: SendGrid Setup (Email Delivery)

SendGrid will handle sending your daily digest emails.

### 1.1 Create SendGrid Account

1. Go to [https://signup.sendgrid.com](https://signup.sendgrid.com)
2. Sign up for a free account
3. Complete email verification
4. Complete the "Tell us about yourself" form (select appropriate options for your use case)

### 1.2 Create API Key

1. Log in to SendGrid dashboard
2. Navigate to **Settings** > **API Keys** (left sidebar)
3. Click **Create API Key** button
4. Enter a name: `OpenAI Frontier Digest`
5. Select **Restricted Access**
6. Under **Mail Send**, toggle it to **FULL ACCESS**
7. Click **Create & View**
8. **IMPORTANT:** Copy your API key NOW - you won't be able to see it again!
   - It will look like: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
9. Save it somewhere safe temporarily (you'll add it to GitHub Secrets in Step 4)

**Screenshot Reference:**
```
Settings > API Keys > Create API Key
Name: OpenAI Frontier Digest
Permissions: Mail Send (Full Access)
```

### 1.3 Verify Sender Identity (Required for Free Tier)

SendGrid requires sender verification on the free tier:

1. Navigate to **Settings** > **Sender Authentication**
2. Choose **Single Sender Verification**
3. Click **Create New Sender**
4. Fill in your information:
   - **From Name:** OpenAI Frontier Digest (or your name)
   - **From Email Address:** Your email (can be the same as recipient)
   - Fill in other required fields
5. Click **Create**
6. Check your email and click the verification link

**Note:** The "From" email address in your digest will match what you set here.

---

## Step 2: NewsAPI Setup (News Gathering)

NewsAPI provides access to news articles from thousands of sources.

### 2.1 Create NewsAPI Account

1. Go to [https://newsapi.org/register](https://newsapi.org/register)
2. Sign up for a free account
3. Verify your email address

### 2.2 Get API Key

1. Log in to NewsAPI dashboard
2. Your API key is displayed on the main dashboard page
3. Copy it - it will look like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
4. Save it temporarily (you'll add it to GitHub Secrets in Step 4)

**Free Tier Limits:**
- 100 requests per day
- News from past 30 days
- Perfect for our daily digest use case

**Note:** If you skip NewsAPI setup, the digest will include a placeholder message. You can configure it later.

---

## Step 3: Create GitHub Repository

### 3.1 Create Repository on GitHub

1. Go to [https://github.com/new](https://github.com/new)
2. Repository settings:
   - **Repository name:** `openai-frontier-digest` (or any name you prefer)
   - **Description:** "Automated daily digest of OpenAI Frontier news"
   - **Visibility:** **Private** (recommended - contains planning docs)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click **Create repository**
4. Keep this page open - you'll need the commands in the next step

### 3.2 Push Your Local Code to GitHub

Open Terminal and navigate to your OpenAI Frontier directory:

```bash
cd "/Users/toddbeavers/OpenAI Frontier"
```

Add all files to git:

```bash
git add .
git commit -m "Initial commit: OpenAI Frontier security readiness and daily digest automation"
```

Connect to your GitHub repository (replace `YOUR_USERNAME` with your GitHub username):

```bash
git remote add origin https://github.com/YOUR_USERNAME/openai-frontier-digest.git
git branch -M main
git push -u origin main
```

**Troubleshooting:**
- If prompted for GitHub credentials, use a [Personal Access Token](https://github.com/settings/tokens) instead of your password
- If you get a 404 error, double-check the repository name and your username

---

## Step 4: Configure GitHub Secrets

GitHub Secrets store sensitive information (API keys) securely.

### 4.1 Navigate to Repository Settings

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/openai-frontier-digest`
2. Click **Settings** tab (far right)
3. In the left sidebar, expand **Secrets and variables**
4. Click **Actions**

### 4.2 Add SENDGRID_API_KEY Secret

1. Click **New repository secret** button
2. Fill in:
   - **Name:** `SENDGRID_API_KEY` (must be exactly this)
   - **Secret:** Paste your SendGrid API key (from Step 1.2)
3. Click **Add secret**

### 4.3 Add RECIPIENT_EMAIL Secret

1. Click **New repository secret** button again
2. Fill in:
   - **Name:** `RECIPIENT_EMAIL` (must be exactly this)
   - **Secret:** `tbeavers12@gmail.com` (or your preferred email)
3. Click **Add secret**

### 4.4 Add NEWSAPI_KEY Secret

1. Click **New repository secret** button again
2. Fill in:
   - **Name:** `NEWSAPI_KEY` (must be exactly this)
   - **Secret:** Paste your NewsAPI key (from Step 2.2)
3. Click **Add secret**

**Important:** Secret names are case-sensitive and must match exactly!

**Final Check:** You should now have 3 secrets:
- ✅ SENDGRID_API_KEY
- ✅ RECIPIENT_EMAIL
- ✅ NEWSAPI_KEY

---

## Step 5: Enable GitHub Actions

GitHub Actions may be disabled by default in private repositories.

### 5.1 Enable Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. If you see a button to enable Actions, click it
4. Select **Allow all actions and reusable workflows**
5. Click **Save**

### 5.2 Verify Workflow File

1. Click **Actions** tab
2. You should see "Daily OpenAI Frontier Digest" in the left sidebar
3. If you see it, you're all set!

---

## Step 6: Test the Digest (Manual Trigger)

Before waiting for the scheduled 7am run, let's test it manually.

### 6.1 Trigger Manual Run

1. Go to **Actions** tab in your repository
2. Click **Daily OpenAI Frontier Digest** in the left sidebar
3. Click the **Run workflow** dropdown button (right side)
4. Click the green **Run workflow** button
5. Wait 30-60 seconds, then refresh the page

### 6.2 Monitor Execution

1. You should see a new workflow run appear (yellow circle = running)
2. Click on the workflow run to view details
3. Click on the **generate-digest** job
4. Expand each step to view logs:
   - ✅ Checkout repository
   - ✅ Set up Python
   - ✅ Install dependencies
   - ✅ Generate and send digest
5. Look for success messages in the logs

### 6.3 Check Your Email

1. Check `tbeavers12@gmail.com` (or your configured email)
2. You should receive an email titled: **"OpenAI Frontier Daily Digest - [Today's Date]"**
3. Verify the email looks good:
   - 3-7 news stories
   - Each story has: title, source, link, summary, why you should care, what it means
   - Proper formatting

### 6.4 Check Local Digest Archive

1. Go to the **Actions** tab > your workflow run
2. Scroll down to **Artifacts** section
3. You'll see **daily-digest-XXX** - this is your saved digest
4. Download it to view the markdown file

**Note:** The `daily-digests/` folder is gitignored and only exists locally or as GitHub Actions artifacts.

---

## Step 7: Verify Scheduled Runs

The digest is scheduled to run automatically every weekday at 7am EST.

### 7.1 Understanding the Schedule

The workflow uses this cron schedule:
```yaml
cron: '0 12 * * 1-5'
```

This means:
- **`0 12`** = 12:00 UTC
- **`* *`** = Every day of month, every month
- **`1-5`** = Monday through Friday

**Timezone Conversion:**
- **Winter (EST):** 12:00 UTC = 7:00 AM EST ✅
- **Summer (EDT):** 12:00 UTC = 8:00 AM EDT ⚠️

### 7.2 Adjusting for Daylight Saving Time

If you want the digest to arrive at 7am year-round:

**Option A: Update cron manually twice a year**
- In March (when DST starts): Change to `'0 11 * * 1-5'` for 7am EDT
- In November (when DST ends): Change to `'0 12 * * 1-5'` for 7am EST

**Option B: Accept 8am during summer**
- Keep `'0 12 * * 1-5'` and receive at 7am EST / 8am EDT

To change the schedule:
1. Edit `.github/workflows/daily-digest.yml`
2. Update the cron value
3. Commit and push changes

### 7.3 Monitoring Scheduled Runs

Check that automated runs are working:

1. Wait until after 7am EST on a weekday
2. Go to **Actions** tab
3. You should see a new automatic run
4. Verify email was received

---

## Step 8: Local Testing (Optional)

For development and testing, you can run the digest locally.

### 8.1 Install Python Dependencies

```bash
cd "/Users/toddbeavers/OpenAI Frontier/scripts"
pip install -r requirements.txt
```

### 8.2 Create Local Environment File

Create a file named `.env` in the `scripts/` directory:

```bash
cd "/Users/toddbeavers/OpenAI Frontier/scripts"
touch .env
```

Edit `.env` and add your API keys:

```
SENDGRID_API_KEY=SG.your_sendgrid_key_here
RECIPIENT_EMAIL=tbeavers12@gmail.com
NEWSAPI_KEY=your_newsapi_key_here
```

**Important:** This file is gitignored and will never be committed.

### 8.3 Run Locally

```bash
cd "/Users/toddbeavers/OpenAI Frontier/scripts"
python generate_digest.py
```

You should see:
- Progress messages
- Stories found and selected
- Digest saved confirmation
- Email sent confirmation

Check your email and the `daily-digests/` folder.

---

## Troubleshooting

### Email Not Received

**Check SendGrid:**
1. Log in to SendGrid dashboard
2. Go to **Activity** to see if email was sent
3. Check for errors or bounces

**Common Issues:**
- ❌ Wrong API key → Regenerate in SendGrid and update GitHub Secret
- ❌ Sender not verified → Complete sender verification (Step 1.3)
- ❌ Email in spam → Add sender to your contacts

### GitHub Actions Failing

**Check Logs:**
1. Go to **Actions** tab
2. Click the failed run
3. Expand steps to see error messages

**Common Issues:**
- ❌ Secrets not set → Verify all 3 secrets exist (Step 4)
- ❌ Secret names wrong → Must be exact: `SENDGRID_API_KEY`, `RECIPIENT_EMAIL`, `NEWSAPI_KEY`
- ❌ Python errors → Check the logs for specific error messages

### No News Stories Found

**Possible Causes:**
- NewsAPI key not configured → Check GitHub Secret `NEWSAPI_KEY`
- No recent OpenAI Frontier news → Normal on some days
- API rate limit reached → Free tier = 100 requests/day

**Fallback:**
If no news is found, the digest will include a configuration message.

### Wrong Timezone

**To adjust:**
1. Edit `.github/workflows/daily-digest.yml`
2. Change cron from `'0 12 * * 1-5'` to your desired UTC time
3. Use [crontab.guru](https://crontab.guru) to verify cron syntax
4. Commit and push changes

---

## Customization

### Change Email Time

Edit `.github/workflows/daily-digest.yml`:

```yaml
schedule:
  - cron: '0 13 * * 1-5'  # 8am EST instead of 7am
```

### Change Number of Stories

Edit `scripts/config.py`:

```python
MIN_STORIES = 5  # Minimum stories (was 3)
MAX_STORIES = 10  # Maximum stories (was 7)
```

### Add More Search Queries

Edit `scripts/config.py`:

```python
SEARCH_QUERIES = [
    'OpenAI Frontier news',
    'OpenAI Frontier enterprise',
    'OpenAI Frontier security',
    'OpenAI Frontier updates',
    'OpenAI Frontier partnership',
    'OpenAI Frontier AI agents',  # Add your own
]
```

### Change Email Format

Edit `scripts/generate_digest.py`, specifically the `generate_digest_markdown()` function to modify the digest structure.

---

## Maintenance

### Weekly Check

Once a week, verify:
- ✅ Emails are arriving daily (Mon-Fri)
- ✅ Stories are relevant
- ✅ No GitHub Actions failures

### Monthly Tasks

Once a month:
- 📊 Review digest quality
- 🔍 Check if search queries need updating
- 🔐 Rotate SendGrid API key (security best practice)
- 📈 Review NewsAPI usage in dashboard

### If You Need to Pause

To temporarily disable the digest:

**Option 1: Disable workflow**
1. Go to **Actions** tab
2. Click **Daily OpenAI Frontier Digest**
3. Click the **•••** menu (top right)
4. Click **Disable workflow**

**Option 2: Comment out the schedule**
Edit `.github/workflows/daily-digest.yml` and comment out the cron line:

```yaml
schedule:
  # - cron: '0 12 * * 1-5'  # Temporarily disabled
```

---

## Security Best Practices

### ✅ Do's

- ✅ Keep API keys in GitHub Secrets only
- ✅ Use private repository for sensitive docs
- ✅ Rotate API keys every 90 days
- ✅ Monitor SendGrid activity for unusual patterns

### ❌ Don'ts

- ❌ Never commit API keys to git
- ❌ Never share your `.env` file
- ❌ Never post API keys in issues or discussions
- ❌ Don't use the same API key for multiple projects

---

## Getting Help

### Resources

- **SendGrid Docs:** [https://docs.sendgrid.com](https://docs.sendgrid.com)
- **NewsAPI Docs:** [https://newsapi.org/docs](https://newsapi.org/docs)
- **GitHub Actions Docs:** [https://docs.github.com/en/actions](https://docs.github.com/en/actions)
- **Cron Schedule Help:** [https://crontab.guru](https://crontab.guru)

### Common Questions

**Q: Can I send to multiple email addresses?**
A: Yes! Modify `scripts/config.py` to add multiple recipients:

```python
RECIPIENT_EMAIL = 'email1@example.com,email2@example.com'
```

**Q: Can I run this more than once per day?**
A: Yes! Add another cron schedule in `.github/workflows/daily-digest.yml`:

```yaml
schedule:
  - cron: '0 12 * * 1-5'  # 7am EST
  - cron: '0 20 * * 1-5'  # 3pm EST
```

**Q: How much does this cost?**
A: $0! Both SendGrid and NewsAPI have generous free tiers that cover this use case.

**Q: What if OpenAI Frontier changes its name or URL?**
A: Update the search queries in `scripts/config.py` to include the new terms.

---

## Success Checklist

Before considering setup complete, verify:

- ✅ GitHub repository created and code pushed
- ✅ SendGrid account created and sender verified
- ✅ NewsAPI account created (optional)
- ✅ All 3 GitHub Secrets configured
- ✅ Manual workflow test successful
- ✅ Email received successfully
- ✅ Email content looks good
- ✅ Scheduled run verified (after first 7am run)

---

## Next Steps

Now that setup is complete:

1. **Wait for first scheduled run** (next weekday at 7am)
2. **Review the digest quality** and adjust search queries if needed
3. **Star this repository** for easy access
4. **Fill out** the security questionnaires in the other markdown files

Enjoy your automated daily digest!

---

**Last Updated:** February 15, 2026
**Version:** 1.0
