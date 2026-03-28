# Quick Start Guide: Security Training Digest

Get your security skills training digest up and running in 20 minutes.

---

## What You'll Get

**Every Friday, Saturday, Sunday at 7am EST:**
- 2-4 curated security training videos (5-15 min each)
- Focus: OIDC, OAuth, MFA, Entra ID, AWS IAM, RBAC, Databricks, Confluent Cloud
- Progressive learning structure building on previous skills
- Email + saved to GitHub Actions artifacts

---

## Prerequisites Checklist

- [ ] GitHub account (free)
- [ ] SendGrid account (free - 100 emails/day)
- [ ] YouTube Data API key (free - 10,000 requests/day)
- [ ] Git installed locally
- [ ] Python 3.11+ (optional, for local testing)

---

## 5-Step Setup

### 1. SendGrid Email Setup (5 min)

```
1. Sign up: https://signup.sendgrid.com
2. Settings > API Keys > Create API Key
   - Name: "Security Training Digest"
   - Permissions: Mail Send (Full Access)
3. Copy API key (starts with SG.)
4. Settings > Sender Authentication > Single Sender Verification
   - Verify your email address
```

**Save:** SendGrid API key

### 2. YouTube Data API Setup (10 min)

```
1. Go to: https://console.cloud.google.com
2. Create new project: "Security Training Digest"
3. APIs & Services > Library
   - Search: "YouTube Data API v3"
   - Click Enable
4. APIs & Services > Credentials
   - Create Credentials > API key
   - Restrict Key > YouTube Data API v3
   - Save
```

**Save:** YouTube API key (starts with AIzaSy)

### 3. Push Code to GitHub (2 min)

```bash
cd "/Users/toddbeavers/OpenAI Frontier"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

### 4. Configure GitHub Secrets (3 min)

Go to: **GitHub Repo > Settings > Secrets and variables > Actions**

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `SENDGRID_API_KEY` | Your SendGrid API key |
| `RECIPIENT_EMAIL` | `tbeavers12@gmail.com` |
| `YOUTUBE_API_KEY` | Your YouTube Data API key |
| `SENDER_EMAIL` | `security-training@skills.com` (optional) |

### 5. Test It (2 min)

```
1. Go to: Actions tab in GitHub
2. Click: "Security Skills Training Digest"
3. Click: "Run workflow" dropdown
4. Click: Green "Run workflow" button
5. Wait 30-60 seconds
6. Check your email!
```

---

## Quick Test: Run Locally

```bash
cd "/Users/toddbeavers/OpenAI Frontier/scripts"

# Create .env file
cat > .env << EOF
SENDGRID_API_KEY=your_sendgrid_key_here
RECIPIENT_EMAIL=tbeavers12@gmail.com
YOUTUBE_API_KEY=your_youtube_key_here
SENDER_EMAIL=security-training@skills.com
EOF

# Install dependencies
pip install -r requirements.txt

# Run digest
python generate_digest.py
```

---

## Verify It's Working

**After manual test:**
- [ ] Email received with subject "🎓 Security Skills Training - [Date]"
- [ ] Contains 2-4 training videos
- [ ] Each video has: title, channel, duration, YouTube link
- [ ] Proper formatting with learning tips

**After first weekend:**
- [ ] Automatic email received Friday/Saturday/Sunday at 7am
- [ ] Check Actions tab for successful runs

---

## Customization Cheat Sheet

### Change Schedule

Edit `.github/workflows/daily-digest.yml`:

```yaml
# Saturdays only at 8am EST
cron: '0 13 * * 6'

# Every day at 7am EST
cron: '0 12 * * *'

# Mon/Wed/Fri at 7am EST
cron: '0 12 * * 1,3,5'
```

### Change Video Count

Edit `scripts/config.py`:

```python
MIN_VIDEOS = 3  # Default: 2
MAX_VIDEOS = 5  # Default: 4
```

### Focus on Different Topics

Edit `scripts/config.py` - Add your search queries:

```python
SEARCH_QUERIES = [
    'Kubernetes security tutorial',
    'Docker security best practices',
    'API security testing video',
    # Add your own...
]
```

---

## Troubleshooting

### No Email Received

```
1. Check SendGrid Activity dashboard for delivery status
2. Verify GitHub Secrets are set correctly
3. Check spam/junk folder
4. Verify sender email is verified in SendGrid
```

### GitHub Action Failed

```
1. Actions tab > Click failed run > View logs
2. Common issues:
   - Missing secret (check all 3-4 are set)
   - Wrong secret names (case-sensitive!)
   - YouTube API not enabled in Google Cloud
   - API key restrictions too strict
```

### No Videos Found

```
1. Verify YouTube API key in GitHub Secrets
2. Check API is enabled: console.cloud.google.com
3. Check API key restrictions (should allow YouTube Data API v3)
4. Verify quota hasn't been exceeded (unlikely)
```

---

## API Quota Reference

**SendGrid Free Tier:**
- 100 emails/day
- 3 per week = 12 per month ✅ Well under limit

**YouTube Data API Free Tier:**
- 10,000 quota units/day
- Each search ~100 units
- 3 digests per week = ~1,200 units/week ✅ Well under limit

---

## Learning Tips

**Maximize Your Learning:**

1. **Take Notes** - Key concepts, commands, configurations
2. **Hands-On Practice** - Try examples in your own environment
3. **Connect the Dots** - How does this apply to your work?
4. **Pace Yourself** - 5-15 min videos = manageable, focused learning
5. **Review Progress** - Download artifacts from GitHub Actions to track your journey

**Progressive Structure:**
- **Weeks 1-2:** Authentication & Authorization fundamentals
- **Weeks 3-4:** OIDC/OAuth flows, Entra ID configuration
- **Weeks 5-6:** Practical RBAC for AWS ↔ Confluent Cloud
- **Weeks 7-8:** Advanced: Just-in-time access, Zero Trust

---

## Files Reference

```
OpenAI Frontier/
├── .github/workflows/
│   └── daily-digest.yml        # Schedule: Fri/Sat/Sun 7am
├── scripts/
│   ├── generate_digest.py      # Main video curation script
│   ├── config.py               # Search queries, video limits
│   └── requirements.txt        # Python dependencies
├── training-digests/           # Local archive (gitignored)
├── SETUP.md                    # Detailed setup guide
├── QUICKSTART.md               # This file
└── README.md                   # Project overview
```

---

## Support Resources

- **Full Setup Guide:** [SETUP.md](./SETUP.md)
- **SendGrid Docs:** https://docs.sendgrid.com
- **YouTube API Docs:** https://developers.google.com/youtube/v3
- **Cron Schedule Help:** https://crontab.guru
- **GitHub Actions Docs:** https://docs.github.com/en/actions

---

## Next Steps

1. ✅ Complete 5-step setup above
2. ⏳ Wait for first scheduled run (Friday/Saturday/Sunday 7am)
3. 📺 Watch videos and take notes
4. 🔧 Adjust search queries based on your learning goals
5. 📈 Track your progress week by week

**Ready for detailed instructions?** → See [SETUP.md](./SETUP.md)

---

**Last Updated:** March 28, 2026
**Version:** 2.0 (Video Curation System)
