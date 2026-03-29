# Setup Tools & Vendor Reference Guide

This document lists all the services and vendors used to set up the Security Skills Training Digest system. Use this as a quick reference for where to log in to make changes, updates, or troubleshoot issues.

---

## 🌐 Domain & DNS Management

### Porkbun (Domain Registrar & DNS)

**What it does:** Domain registration and DNS management for whollyground.io

**Login URL:** https://porkbun.com/account/domainsSpeedy

**What's configured here:**
- Domain registration: whollyground.io
- DNS records for email (MX, SPF, DKIM, DMARC)
- DNS records for SendGrid (CNAME records for domain authentication)

**DNS Records Summary:**
- **MX Records:** 3 records pointing to Zoho Mail (mx.zoho.com, mx2.zoho.com, mx3.zoho.com)
- **TXT Records:** SPF, DKIM (zmail._domainkey), DMARC (_dmarc)
- **CNAME Records:** 3 records for SendGrid (em9605, s1._domainkey, s2._domainkey)

**When to access:**
- Add/modify DNS records
- Update domain settings
- Renew domain registration
- Check DNS propagation issues

---

## 📧 Email Services

### Zoho Mail (Email Hosting)

**What it does:** Email hosting and management for toddfathor@whollyground.io

**Login URLs:**
- **Mail Access:** https://mail.zoho.com/
- **Admin Console:** https://mailadmin.zoho.com/

**What's configured here:**
- Email account: toddfathor@whollyground.io
- Domain verification
- Email forwarding rules (if any)
- Spam filters

**Credentials:**
- Email: toddfathor@whollyground.io
- Password: [Your Zoho password]

**When to access:**
- Check email
- Verify SendGrid sender emails
- Update email settings
- Check DNS verification status
- Manage spam/filters

---

### SendGrid (Email Sending Service)

**What it does:** Sends the automated security training digest emails

**Login URL:** https://app.sendgrid.com/

**What's configured here:**
- Domain Authentication: whollyground.io (verified)
- API Key: Security Training Digest (restricted access - Mail Send only)
- Sender: toddfathor@whollyground.io

**API Key Location:** Stored in GitHub Secrets as `SENDGRID_API_KEY`

**When to access:**
- Create/regenerate API keys
- Check email delivery status (Activity dashboard)
- View email statistics
- Add additional verified senders
- Troubleshoot email delivery issues

**Important Pages:**
- Settings → API Keys (manage keys)
- Settings → Sender Authentication (domain verification)
- Activity (email delivery logs)

**Free Tier Limits:**
- 100 emails per day
- Current usage: ~3 emails per week

---

## 🎥 Video API

### Google Cloud Console (YouTube Data API)

**What it does:** Provides access to YouTube API for searching security training videos

**Login URL:** https://console.cloud.google.com/

**What's configured here:**
- Project: "Security Training Digest"
- YouTube Data API v3 (enabled)
- API Key: Restricted to YouTube Data API v3

**API Key:** `AIzaSyD_9ewaiOyMaWEtBUR7v1-9NyI5gpsKO7s`
**Stored in:** GitHub Secrets as `YOUTUBE_API_KEY`

**When to access:**
- Check API quota usage (10,000 units/day)
- Regenerate API key if needed
- View API usage statistics
- Enable/disable APIs

**Navigation:**
- APIs & Services → Credentials (manage API keys)
- APIs & Services → Enabled APIs (view YouTube Data API v3)
- APIs & Services → Dashboard (usage statistics)

**Free Tier Limits:**
- 10,000 quota units per day
- Current usage: ~100-200 units per digest (3x per week)

---

## 🔧 Development & Automation

### GitHub (Code Repository & Automation)

**What it does:** Hosts code and runs automated workflows via GitHub Actions

**Login URL:** https://github.com/

**Repository:** https://github.com/Todd-Father/OpenAI-Frontier

**What's configured here:**
- Source code for digest generation
- GitHub Actions workflow (runs Fri/Sat/Sun at 7am EST)
- GitHub Secrets (API keys and configuration)

**GitHub Secrets (Settings → Secrets → Actions):**
```
SENDGRID_API_KEY    = SG.xxxxxxxx... (SendGrid API key)
SENDER_EMAIL        = toddfathor@whollyground.io
RECIPIENT_EMAIL     = tbeavers12@gmail.com
YOUTUBE_API_KEY     = lol-9NyI5gpsKO2247x
```

**When to access:**
- Update code/configuration
- View workflow runs and logs
- Update GitHub Secrets
- Manually trigger workflow runs
- Check for workflow errors

**Important Pages:**
- Actions → Security Skills Training Digest (workflow runs)
- Settings → Secrets and variables → Actions (secrets)
- Code → .github/workflows/daily-digest.yml (workflow config)

**Workflow Schedule:**
- Runs automatically: Friday, Saturday, Sunday at 7:00 AM EST
- Cron: `0 12 * * 0,5,6` (12:00 UTC = 7am EST)

---

## 📬 Email Recipients

### Gmail (Recipient Email)

**What it does:** Receives the security training digest emails

**Login URL:** https://mail.google.com/

**Email:** tbeavers12@gmail.com

**When to access:**
- Read digest emails
- Check if emails are being delivered
- Move emails out of spam (if needed)
- Verify email formatting looks correct

---

## 🔄 Service Dependencies

```
GitHub Actions (runs workflow)
    ↓
YouTube Data API (searches for videos)
    ↓
Python Script (generates digest)
    ↓
SendGrid (sends email)
    ↓
Gmail (receives email)

DNS Flow:
Porkbun (DNS records)
    ↓
    ├─→ Zoho Mail (MX records for email hosting)
    └─→ SendGrid (CNAME records for domain authentication)
```

---

## 📊 Quick Reference Table

| Service | Purpose | Login URL | API Key Location |
|---------|---------|-----------|-----------------|
| **Porkbun** | Domain & DNS | https://porkbun.com/account/domainsSpeedy | N/A |
| **Zoho Mail** | Email hosting | https://mail.zoho.com/ | N/A |
| **SendGrid** | Email sending | https://app.sendgrid.com/ | GitHub Secrets |
| **Google Cloud** | YouTube API | https://console.cloud.google.com/ | GitHub Secrets |
| **GitHub** | Code & automation | https://github.com/Todd-Father/OpenAI-Frontier | N/A |
| **Gmail** | Email recipient | https://mail.google.com/ | N/A |

---

## 🔐 Security Notes

**API Keys & Passwords:**
- Never commit API keys to git
- Store sensitive credentials in GitHub Secrets only
- Rotate API keys every 90 days (recommended)
- Use strong, unique passwords for each service

**Where Secrets Are Stored:**
- ✅ GitHub Secrets (encrypted, safe)
- ✅ Password manager (recommended for login passwords)
- ❌ Never in code files
- ❌ Never in plain text documents

---

## 🆘 Common Troubleshooting

### Email Not Sending
**Check:**
1. SendGrid Activity dashboard for errors
2. GitHub Actions logs for failures
3. GitHub Secrets are set correctly

### Videos Not Found
**Check:**
1. YouTube API quota in Google Cloud Console
2. API key is valid in GitHub Secrets

### DNS Issues
**Check:**
1. Porkbun DNS records are correct
2. Wait 1 hour for DNS propagation
3. Use https://mxtoolbox.com/ to verify

### Workflow Not Running
**Check:**
1. GitHub Actions are enabled
2. Workflow file syntax is correct
3. Scheduled time is correct (UTC vs EST)

---

## 📅 Maintenance Schedule

**Monthly:**
- [ ] Review SendGrid email delivery stats
- [ ] Check YouTube API quota usage
- [ ] Verify all services are working

**Quarterly (Every 3 Months):**
- [ ] Rotate SendGrid API key
- [ ] Review and update search queries (config.py)
- [ ] Check domain expiration date in Porkbun

**Annually:**
- [ ] Renew whollyground.io domain in Porkbun
- [ ] Review all service free tier limits
- [ ] Update documentation

---

## 📝 Change Log

| Date | Change | Service |
|------|--------|---------|
| 2026-03-28 | Initial setup completed | All services |
| 2026-03-28 | Domain authentication verified | SendGrid |
| 2026-03-28 | DNS records configured | Porkbun |
| 2026-03-28 | Email hosting setup | Zoho Mail |

---

**Last Updated:** March 28, 2026
**System Status:** ✅ Operational
**Next Scheduled Digest:** Friday, 7:00 AM EST
