# How to Build Your Own Automated Daily News Digest (For Any Topic) - $0/Month

**Stop scrolling through endless search results. Let automation bring the news to you.**

---

## The Problem

Whether you're tracking AI developments, cybersecurity threats, regulatory changes, or your competitor's moves, staying informed is exhausting. You know you should check daily, but between meetings, emails, and actual work, that 30-minute research session keeps getting pushed to tomorrow.

What if the news came to you—curated, ranked, and delivered to your inbox every morning?

## What We're Building

A fully automated system that:
- Runs every weekday at a time you choose (e.g., 7 AM)
- Searches for articles about YOUR topic using NewsAPI
- Ranks stories by relevance, recency, and source quality
- Generates a formatted digest with summaries and insights
- Emails it to you via SendGrid
- Costs exactly **$0/month** using free tiers

**Real example:** I built this for OpenAI Frontier news. Every morning at 7 AM, I get 3-7 top stories with:
- Article title and source
- Brief summary
- "Why You Should Care" analysis
- "What This Means" strategic context
- Direct links to full articles

Total time to read: **2 minutes**.
Time saved vs. manual research: **28 minutes/day**.
That's **10+ hours per month** back in your calendar.

---

## The Stack (All Free)

| Tool | Purpose | Free Tier | Cost |
|------|---------|-----------|------|
| **GitHub Actions** | Automation engine | 2,000 min/month | $0 |
| **SendGrid** | Email delivery | 100 emails/day | $0 |
| **NewsAPI** | News aggregation | 100 requests/day | $0 |
| **Python** | Scripting | Unlimited | $0 |
| **GitHub** | Code hosting | Unlimited public/private repos | $0 |

**Total monthly cost: $0**

---

## Prerequisites

**Time Required:** 60-90 minutes (one-time setup)

**Skills Needed:**
- Basic command line comfort
- Ability to copy/paste code (seriously, that's it)
- GitHub account
- Email address

**You DON'T need:**
- A server
- A credit card
- Advanced programming skills
- DevOps experience

---

## Step-by-Step Tutorial

### Part 1: Define Your Topic (5 minutes)

**What do you want to track?**

Examples:
- **Industry:** "Cybersecurity threats," "Fintech innovation," "Healthcare AI"
- **Technology:** "Kubernetes updates," "Rust programming," "Web3 developments"
- **Company:** "Microsoft Azure," "Your competitor name," "Startup funding"
- **Regulatory:** "GDPR compliance," "SEC regulations," "FDA approvals"
- **Niche:** "Sustainable fashion," "Indoor farming," "Quantum computing"

**My example:** "OpenAI Frontier" (enterprise AI platform)

**Your turn:**
```
My topic: _______________________________________
```

**Write 3-5 search queries** that capture your topic:
```
1. _______________________________________
2. _______________________________________
3. _______________________________________
4. _______________________________________
5. _______________________________________
```

### Part 2: Set Up NewsAPI (10 minutes)

**Step 1: Create Account**
1. Go to [newsapi.org/register](https://newsapi.org/register)
2. Sign up with your email
3. Verify your email
4. You'll see your API key immediately on the dashboard

**Step 2: Test Your Searches**
1. Go to [newsapi.org/docs/endpoints/everything](https://newsapi.org/docs/endpoints/everything)
2. Enter your first search query
3. Click "Send Request"
4. Review the results—are these the articles you want?
5. Adjust your queries if needed

**Step 3: Save Your API Key**
- Copy your 32-character API key
- Save it temporarily (you'll add it to GitHub Secrets later)

**Free Tier:** 100 requests/day (perfect for 1 daily digest per topic)

### Part 3: Set Up SendGrid (15 minutes)

**Step 1: Create Account**
1. Go to [sendgrid.com/pricing](https://sendgrid.com/pricing)
2. Click "Try for Free"
3. Sign up and verify your email
4. Complete onboarding questions

**Step 2: Verify Your Sender Email** (Critical!)
1. Go to [Settings → Sender Authentication](https://app.sendgrid.com/settings/sender_auth/senders)
2. Click "Verify a Single Sender"
3. Fill in the form:
   - **From Email:** Your email address (can be Gmail, Outlook, etc.)
   - **From Name:** "[Your Topic] Daily Digest"
   - **Reply To:** Same as From Email
   - Fill in address details (required but not shown in emails)
4. Click "Create"
5. **Check your email inbox**
6. Click verification link
7. Return to SendGrid—you should see a **green checkmark** ✅

**Step 3: Create API Key**
1. Go to [Settings → API Keys](https://app.sendgrid.com/settings/api_keys)
2. Click "Create API Key"
3. Name: "Daily Digest"
4. Permissions: **"Full Access"** (easiest for beginners)
5. Click "Create & View"
6. **COPY THE ENTIRE KEY** (starts with `SG.`, about 69 characters)
7. Save it temporarily (you'll add it to GitHub Secrets later)

**Free Tier:** 100 emails/day (you'll send 1/day = ~22/month)

### Part 4: Fork or Clone the Base Code (10 minutes)

**Option A: Use My Template (Easiest)**

I've created a template repository you can fork:

1. Go to [github.com/YOUR_USERNAME/daily-digest-template](https://github.com) (fictional link for now)
2. Click "Use this template" → "Create a new repository"
3. Name it: `my-topic-digest` (replace with your topic)
4. Choose **Private** (recommended)
5. Click "Create repository"

**Option B: Build From Scratch**

If you prefer to understand every piece:

1. Create new GitHub repository
2. Create this file structure:
```
my-topic-digest/
├── .github/
│   └── workflows/
│       └── daily-digest.yml
├── scripts/
│   ├── generate_digest.py
│   ├── config.py
│   └── requirements.txt
├── .gitignore
└── README.md
```

I'll provide the code for each file below.

### Part 5: Customize the Configuration (15 minutes)

**Edit `scripts/config.py`:**

```python
import os

# === CUSTOMIZE THIS SECTION ===

# Email configuration
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'your.email@example.com')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'your.email@example.com')
SENDER_NAME = 'Your Topic Daily Digest'  # Change this!
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Search configuration - CHANGE THESE TO YOUR TOPIC!
SEARCH_QUERIES = [
    'your topic here',
    'another query about your topic',
    'related search term',
]

# Story limits
MIN_STORIES = 3  # Minimum stories to include
MAX_STORIES = 7  # Maximum stories to include

# === ADVANCED CUSTOMIZATION (OPTIONAL) ===

# Authoritative sources (articles from these get higher priority)
AUTHORITATIVE_SOURCES = [
    'techcrunch.com',
    'reuters.com',
    'bloomberg.com',
    'wired.com',
    # Add sources relevant to YOUR topic
]

# Email subject line
EMAIL_SUBJECT_TEMPLATE = "Your Topic Daily Digest - {date}"

# Local storage folder (gitignored)
DIGEST_FOLDER = 'daily-digests'
```

**What to change:**
1. `SENDER_NAME` - Your digest name (e.g., "Cybersecurity Daily Digest")
2. `SEARCH_QUERIES` - Your 3-5 search terms from Part 1
3. `EMAIL_SUBJECT_TEMPLATE` - Your subject line
4. `AUTHORITATIVE_SOURCES` - Add news sites relevant to your topic

**Leave these as-is:**
- `RECIPIENT_EMAIL`, `SENDER_EMAIL`, `SENDGRID_API_KEY` - These pull from GitHub Secrets
- `MIN_STORIES`, `MAX_STORIES` - Default values work well

### Part 6: Set Your Schedule (5 minutes)

**Edit `.github/workflows/daily-digest.yml`:**

Find this line:
```yaml
- cron: '0 12 * * 1-5'  # 7am EST Monday-Friday
```

**Change the time:**
- `'0 12 * * 1-5'` = 7am EST (12pm UTC)
- `'0 13 * * 1-5'` = 8am EST (1pm UTC)
- `'0 14 * * 1-5'` = 9am EST (2pm UTC)

**Change the days:**
- `1-5` = Monday-Friday
- `1-7` = Every day
- `1,3,5` = Mon, Wed, Fri only

**Tool:** Use [crontab.guru](https://crontab.guru) to create custom schedules

### Part 7: Add GitHub Secrets (10 minutes)

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add each:

**Secret 1:**
- Name: `SENDGRID_API_KEY`
- Value: Your SendGrid API key (from Part 3)

**Secret 2:**
- Name: `RECIPIENT_EMAIL`
- Value: Your email address

**Secret 3:**
- Name: `NEWSAPI_KEY`
- Value: Your NewsAPI key (from Part 2)

**Secret 4:**
- Name: `SENDER_EMAIL`
- Value: Your verified sender email (from Part 3)

### Part 8: Test Your Digest (5 minutes)

1. Go to **Actions** tab in your repository
2. Click "Daily Digest" (or whatever you named your workflow)
3. Click **"Run workflow"** dropdown → **"Run workflow"** button
4. Wait 30-60 seconds
5. Click on the workflow run to view logs
6. Look for: `Email sent successfully! Status code: 202`
7. **Check your email inbox!**

**Troubleshooting:**
- If you see `403 Forbidden`: Sender email not verified
- If you see `No articles found`: Adjust your search queries
- If you see `AttributeError`: Copy my latest code (I fixed this bug!)

---

## Advanced Customization

### Change the Digest Format

**Edit `scripts/generate_digest.py`, find the `generate_digest_markdown` function:**

```python
digest += f"""## {i}. {title}

**Source:** {source} | **[Read Full Article]({url})**

**Summary:** {description}

**Why You Should Care:** {why_care}

**What This Means:** {what_means}

---
"""
```

**Customize it:**
- Remove "Why You Should Care" if you just want summaries
- Add author name if available
- Change formatting (bullets instead of paragraphs)
- Add emoji 📰 🔥 ⚡ for visual interest

### Add Filtering by Date Range

Want only articles from the past 24 hours?

**Edit `scripts/generate_digest.py`, find `_search_newsapi` function:**

```python
from_date = to_date - timedelta(days=1)  # Change from 2 to 1
```

### Customize the Ranking Algorithm

**Edit `scripts/generate_digest.py`, find `analyze_and_rank_stories` function:**

Adjust scoring:
```python
# Current scoring:
# Exact topic match: +10 points
# Authoritative source: +5 points
# Past 24 hours: +5 points
# Past 48 hours: +3 points
# Long content: +3 points
# Keywords: +2 points each

# You can change these numbers or add your own criteria!
```

### Multiple Topics in One Digest

Want to track 2-3 related topics?

**Edit `config.py`:**
```python
SEARCH_QUERIES = [
    # Topic 1
    'artificial intelligence regulation',
    'AI governance',
    # Topic 2
    'machine learning security',
    'AI vulnerabilities',
    # Topic 3
    'enterprise AI adoption',
]
```

The digest will include articles from all queries, ranked together.

### Add a Weekly Summary

Want a special Friday email with the week's highlights?

**Edit `.github/workflows/daily-digest.yml`:**

Add a second cron schedule:
```yaml
schedule:
  - cron: '0 12 * * 1-4'  # Mon-Thu: daily digest
  - cron: '0 13 * * 5'    # Friday: weekly summary (runs 1 hour later)
```

Then detect Friday in your Python script and generate a different format.

---

## Real-World Use Cases

### 1. Competitive Intelligence
**Topic:** "Competitor name product launches"
**Frequency:** Daily
**Result:** Never miss a competitor announcement

### 2. Regulatory Compliance
**Topic:** "GDPR enforcement actions"
**Frequency:** Daily
**Result:** Stay ahead of compliance risks

### 3. Technology Trends
**Topic:** "Kubernetes best practices"
**Frequency:** Mon/Wed/Fri
**Result:** Level up your DevOps skills passively

### 4. Investment Research
**Topic:** "Fintech startup funding"
**Frequency:** Daily
**Result:** Spot emerging opportunities early

### 5. Academic Research
**Topic:** "Quantum computing breakthroughs"
**Frequency:** Daily
**Result:** Track your research field effortlessly

---

## Cost Breakdown & Scaling

### Current Setup (1 Topic)
- **GitHub Actions:** ~5 min/day × 22 days = ~110 min/month (free tier: 2,000)
- **SendGrid:** ~22 emails/month (free tier: 3,000/month or 100/day)
- **NewsAPI:** ~22 requests/month (free tier: 100/day)
- **Total Cost:** $0

### Scaling to Multiple Topics

**3 Topics:**
- GitHub Actions: ~330 min/month (still free)
- SendGrid: ~66 emails/month (still free)
- NewsAPI: ~66 requests/month (still free)
- **Total Cost:** $0

**10 Topics:**
- GitHub Actions: ~1,100 min/month (still free)
- SendGrid: ~220 emails/month (still free)
- NewsAPI: ~220 requests/month (still free)
- **Total Cost:** $0

**When you'd need to pay:**
- NewsAPI: >100 requests/day = ~$450/month (Business tier)
- SendGrid: >100 emails/day = $20/month (Essentials tier)
- GitHub Actions: >2,000 min/month = $0.008/min after

**Recommendation:** Stick with 1-3 topics on free tier!

---

## Maintenance & Troubleshooting

### Weekly Checks
- [ ] Verify email arrived Monday-Friday
- [ ] Scan for repeated/irrelevant articles
- [ ] Adjust search queries if quality drops

### Monthly Tasks
- [ ] Review GitHub Actions usage (should be <1,000 min)
- [ ] Rotate SendGrid API key (security best practice)
- [ ] Check NewsAPI usage (should be <100/day)

### Common Issues

**1. No email received**
- Check GitHub Actions logs for errors
- Verify secrets are set correctly
- Check spam folder

**2. Irrelevant articles**
- Refine search queries to be more specific
- Add negative keywords (if NewsAPI supports)
- Adjust authoritative sources list

**3. Workflow not running**
- Verify GitHub Actions is enabled
- Check cron schedule timezone conversion
- Ensure repository isn't archived

**4. Rate limits exceeded**
- Reduce frequency (every other day instead of daily)
- Narrow search queries
- Consider upgrading to paid tier

---

## Next Steps & Ideas

### Level 1: Working Digest
✅ Basic automation running
✅ Daily emails arriving
✅ Content is relevant

### Level 2: Optimization
- [ ] Fine-tune search queries based on 1 week of results
- [ ] Customize digest format to your preferences
- [ ] Add more authoritative sources

### Level 3: Advanced Features
- [ ] Add sentiment analysis (positive/negative news)
- [ ] Include trending score (viral articles)
- [ ] Archive digests to Notion or Airtable
- [ ] Share digest with your team (multiple recipients)

### Level 4: Power User
- [ ] Multiple topics, separate digests
- [ ] Weekly summary on Fridays
- [ ] Integration with Slack/Teams
- [ ] Custom ML model for relevance scoring

---

## The Template Code

### `scripts/generate_digest.py` (Core Script)

I won't paste the full 491-line script here, but it's structured as:

```python
#!/usr/bin/env python3
"""
Daily Digest Generator

Searches for news, ranks by relevance, generates digest, sends email.
"""

# Main functions:
# 1. search_newsapi() - Gets articles from NewsAPI
# 2. analyze_and_rank_stories() - Scores and ranks by relevance
# 3. generate_digest_markdown() - Creates formatted digest
# 4. save_digest_locally() - Saves to daily-digests/ folder
# 5. send_email_via_sendgrid() - Sends via SendGrid API
# 6. main() - Orchestrates the flow
```

**Get the full code:**
- Fork my repository: [github.com/Todd-Father/OpenAI-Frontier](https://github.com/Todd-Father/OpenAI-Frontier)
- Or contact me for the template

### `.github/workflows/daily-digest.yml` (GitHub Actions)

```yaml
name: Daily Digest

on:
  schedule:
    - cron: '0 12 * * 1-5'  # 7am EST Mon-Fri
  workflow_dispatch:  # Manual trigger

jobs:
  generate-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r scripts/requirements.txt
      - name: Generate and send digest
        env:
          SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}
          RECIPIENT_EMAIL: ${{ secrets.RECIPIENT_EMAIL }}
          NEWSAPI_KEY: ${{ secrets.NEWSAPI_KEY }}
          SENDER_EMAIL: ${{ secrets.SENDER_EMAIL }}
        run: python scripts/generate_digest.py
```

### `scripts/requirements.txt`

```
sendgrid>=6.11.0
python-dotenv>=1.0.0
requests>=2.31.0
markdown>=3.5.0
```

---

## Conclusion

**You just built a personal AI research assistant for $0/month.**

This isn't just about saving time—it's about consistency. When you automate daily research, you never miss important developments. You spot trends early. You make better-informed decisions.

And the best part? You built something you can iterate on forever. Add features, refine queries, expand to new topics. It's yours.

**Time investment:** 60-90 minutes (one-time)
**Time saved:** 28 minutes/day = 10+ hours/month
**Payback period:** ~3 days

**What will you track?**

---

## Resources

### Official Documentation
- [SendGrid API Docs](https://docs.sendgrid.com)
- [NewsAPI Documentation](https://newsapi.org/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

### Tools & Utilities
- [Crontab.guru](https://crontab.guru) - Cron schedule builder
- [Markdown Guide](https://www.markdownguide.org) - Format your digests
- [Regex101](https://regex101.com) - Test search patterns

### Community
- Share your digest setups with #DailyDigest
- Join GitHub Discussions for troubleshooting
- Fork and improve the template

---

## About the Author

I built this system to track OpenAI Frontier developments for an enterprise partnership. The automation saves me 10+ hours per month and ensures I never miss critical updates.

**My setup:**
- **Topic:** OpenAI Frontier enterprise AI platform
- **Frequency:** Weekdays at 7 AM EST
- **Sources:** TechCrunch, Reuters, OpenAI Blog, Wired, Forbes, Bloomberg
- **Result:** 3-7 curated stories with strategic analysis

**Want to see it in action?** Check out my repository or connect with me to discuss automation strategies for professional intelligence gathering.

---

**Build your digest today. Your future self will thank you.** 🚀

---

**Last Updated:** February 16, 2026
**Difficulty:** Beginner-Friendly
**Time to Complete:** 60-90 minutes
**Ongoing Effort:** <5 minutes/month

**Tags:** #Automation #Productivity #NewsAPI #SendGrid #GitHubActions #Python #NoCode #FreeTier #OpenSource
