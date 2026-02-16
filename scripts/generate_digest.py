#!/usr/bin/env python3
"""
OpenAI Frontier Daily Digest Generator

This script searches for OpenAI Frontier news, analyzes and ranks stories,
generates a digest, saves it locally, and emails it via SendGrid.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
import markdown

# Load environment variables from .env file (for local testing)
load_dotenv()

# Import configuration
import config


def search_openai_frontier_news():
    """
    Search for recent OpenAI Frontier news articles.

    Uses web search to find articles from the past 24-48 hours.
    Returns list of articles with title, URL, source, date, and snippet.
    """
    print("Searching for OpenAI Frontier news...")

    articles = []

    # Method 1: Use NewsAPI (requires API key)
    newsapi_key = os.getenv('NEWSAPI_KEY')
    if newsapi_key:
        articles.extend(_search_newsapi(newsapi_key))

    # Method 2: Manual RSS/scraping fallback (add your preferred sources)
    # This is a fallback if NewsAPI is not configured
    if not articles:
        print("WARNING: No news API configured. Using fallback method...")
        articles = _get_fallback_articles()

    print(f"Found {len(articles)} articles")
    return articles


def _search_newsapi(api_key):
    """Search using NewsAPI"""
    articles = []

    # Calculate date range (past 2 days to catch more stories)
    to_date = datetime.now()
    from_date = to_date - timedelta(days=2)

    url = "https://newsapi.org/v2/everything"

    for query in config.SEARCH_QUERIES:
        params = {
            'q': query,
            'from': from_date.strftime('%Y-%m-%d'),
            'to': to_date.strftime('%Y-%m-%d'),
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': api_key,
            'pageSize': 10
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'ok':
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', 'No title'),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'published_at': article.get('publishedAt', ''),
                        'description': article.get('description', ''),
                        'content': article.get('content', '')
                    })
        except Exception as e:
            print(f"Error searching NewsAPI for '{query}': {e}")
            continue

    return articles


def _get_fallback_articles():
    """
    Fallback method when no news API is configured.
    Returns placeholder articles with instructions.
    """
    return [{
        'title': 'NewsAPI Configuration Required',
        'url': 'https://newsapi.org',
        'source': 'System',
        'published_at': datetime.now().isoformat(),
        'description': 'To receive real-time OpenAI Frontier news, please configure NewsAPI. See SETUP.md for instructions.',
        'content': 'Get your free API key at https://newsapi.org and add it to your GitHub Secrets as NEWSAPI_KEY.'
    }]


def analyze_and_rank_stories(articles):
    """
    Analyze and rank articles by relevance.

    Scoring criteria:
    - Mentions "OpenAI Frontier" explicitly (+10)
    - From authoritative source (+5)
    - Recent (past 24h: +5, past 48h: +3)
    - Long content (+3)
    - Contains keywords: enterprise, security, partnership (+2 each)

    Returns top MIN_STORIES to MAX_STORIES ranked articles.
    """
    print(f"Analyzing and ranking {len(articles)} articles...")

    scored_articles = []

    for article in articles:
        score = 0

        # Combine title, description, and content for analysis
        title = article.get('title') or ''
        description = article.get('description') or ''
        content = article.get('content') or ''
        full_text = f"{title} {description} {content}".lower()

        # Check for "OpenAI Frontier" mention (high priority)
        if 'openai frontier' in full_text:
            score += 10
        elif 'frontier' in full_text and 'openai' in full_text:
            score += 7  # Both words present but not together

        # Check if from authoritative source
        source_domain = _extract_domain(article.get('url', ''))
        if any(auth_source in source_domain for auth_source in config.AUTHORITATIVE_SOURCES):
            score += 5

        # Check recency
        published_at = article.get('published_at', '')
        if published_at:
            try:
                pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                hours_ago = (datetime.now() - pub_date.replace(tzinfo=None)).total_seconds() / 3600

                if hours_ago < 24:
                    score += 5
                elif hours_ago < 48:
                    score += 3
            except:
                pass

        # Check content length
        if len(content) > 500:
            score += 3

        # Check for important keywords
        keywords = ['enterprise', 'security', 'partnership', 'customer', 'integration']
        for keyword in keywords:
            if keyword in full_text:
                score += 2

        scored_articles.append({
            'article': article,
            'score': score
        })

    # Sort by score (highest first)
    scored_articles.sort(key=lambda x: x['score'], reverse=True)

    # Remove duplicates by URL
    seen_urls = set()
    unique_articles = []
    for item in scored_articles:
        url = item['article'].get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(item)

    # Return top MIN_STORIES to MAX_STORIES
    top_articles = unique_articles[:config.MAX_STORIES]

    # Filter to only articles with meaningful scores
    meaningful_articles = [item for item in top_articles if item['score'] > 0]

    if len(meaningful_articles) < config.MIN_STORIES:
        print(f"WARNING: Only found {len(meaningful_articles)} relevant articles (minimum is {config.MIN_STORIES})")
        # Return what we have
        return [item['article'] for item in top_articles[:config.MIN_STORIES]]

    print(f"Selected top {len(meaningful_articles)} articles")
    return [item['article'] for item in meaningful_articles]


def _extract_domain(url):
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc.lower()
    except:
        return ''


def generate_digest_markdown(stories, date):
    """
    Generate formatted markdown digest.

    Format includes:
    - Header with date
    - For each story: title, source, link, summary, why care, what it means
    - Footer with metadata
    """
    print(f"Generating digest for {len(stories)} stories...")

    date_str = date.strftime('%B %d, %Y')

    digest = f"""# OpenAI Frontier Daily Digest
**{date_str}**

---

"""

    for i, story in enumerate(stories, 1):
        title = story.get('title') or 'No title'
        source = story.get('source') or 'Unknown'
        url = story.get('url') or '#'
        description = story.get('description') or 'No description available'

        # Generate "Why You Should Care" and "What This Means"
        why_care, what_means = _generate_insights(story)

        digest += f"""## {i}. {title}

**Source:** {source} | **[Read Full Article]({url})**

**Summary:** {description}

**Why You Should Care:** {why_care}

**What This Means:** {what_means}

---

"""

    # Add footer
    digest += f"""
---

*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M UTC')}*

**About This Digest:** This automated digest tracks news and developments related to OpenAI Frontier,
the enterprise AI agent platform launched in February 2026. Stories are selected based on relevance,
source authority, and recency.

**Feedback or Questions?** Reply to this email.
"""

    return digest


def _generate_insights(story):
    """
    Generate "Why You Should Care" and "What This Means" insights.

    Uses heuristics based on content to provide context.
    """
    title = (story.get('title') or '').lower()
    description = (story.get('description') or '').lower()
    content = (story.get('content') or '').lower()
    full_text = f"{title} {description} {content}"

    # Why You Should Care
    why_care = ""
    if any(word in full_text for word in ['security', 'breach', 'vulnerability', 'risk']):
        why_care = "Security implications for enterprise AI deployments may affect your OpenAI Frontier implementation strategy."
    elif any(word in full_text for word in ['partnership', 'integration', 'customer']):
        why_care = "New partnerships and integrations could expand Frontier's capabilities and ecosystem."
    elif any(word in full_text for word in ['feature', 'update', 'release', 'launch']):
        why_care = "New features or updates may enhance your organization's AI agent capabilities."
    elif any(word in full_text for word in ['compliance', 'regulation', 'gdpr', 'privacy']):
        why_care = "Regulatory developments may impact how you deploy and govern AI agents."
    else:
        why_care = "This development may influence enterprise AI strategy and OpenAI Frontier adoption."

    # What This Means
    what_means = ""
    if any(word in full_text for word in ['enterprise', 'business', 'customer']):
        what_means = "Enterprise adoption patterns are evolving, potentially validating or challenging your implementation approach."
    elif any(word in full_text for word in ['competition', 'competitor', 'alternative']):
        what_means = "The competitive landscape is shifting, which may affect feature development and pricing."
    elif any(word in full_text for word in ['technical', 'capability', 'performance']):
        what_means = "Technical capabilities are advancing, potentially enabling new use cases for your organization."
    else:
        what_means = "Monitor how this development aligns with your organization's OpenAI Frontier roadmap."

    return why_care, what_means


def save_digest_locally(digest, date):
    """
    Save digest to local daily-digests/ folder.

    Filename format: YYYY-MM-DD.md
    """
    print("Saving digest locally...")

    # Create digest folder if it doesn't exist
    digest_folder = Path(config.DIGEST_FOLDER)
    digest_folder.mkdir(exist_ok=True)

    # Generate filename
    filename = f"{date.strftime('%Y-%m-%d')}.md"
    filepath = digest_folder / filename

    # Write digest
    try:
        filepath.write_text(digest, encoding='utf-8')
        print(f"Digest saved to: {filepath}")
        return str(filepath)
    except Exception as e:
        print(f"Error saving digest: {e}")
        return None


def send_email_via_sendgrid(digest, date, recipient):
    """
    Send digest email via SendGrid.

    Sends both HTML and plain text versions.
    """
    print(f"Sending email to {recipient}...")

    api_key = config.SENDGRID_API_KEY
    if not api_key:
        print("ERROR: SENDGRID_API_KEY not set. Email not sent.")
        print("To test locally, create a .env file with SENDGRID_API_KEY=your_key")
        return False

    # Convert markdown to HTML
    html_content = markdown.markdown(digest)

    # Create styled HTML email
    html_email = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ecf0f1;
                margin: 30px 0;
            }}
            .footer {{
                background-color: #f8f9fa;
                padding: 20px;
                margin-top: 40px;
                border-radius: 5px;
                font-size: 0.9em;
                color: #666;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Create SendGrid message
    subject = config.EMAIL_SUBJECT_TEMPLATE.format(date=date.strftime('%B %d, %Y'))

    message = Mail(
        from_email=(config.SENDER_EMAIL, config.SENDER_NAME),
        to_emails=recipient,
        subject=subject
    )

    # Add both plain text and HTML content
    message.add_content(Content("text/plain", digest))
    message.add_content(Content("text/html", html_email))

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(f"Email sent successfully! Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def main():
    """
    Main execution function.

    1. Search for news
    2. Analyze and rank
    3. Generate digest
    4. Save locally
    5. Send email
    """
    print("=" * 60)
    print("OpenAI Frontier Daily Digest Generator")
    print("=" * 60)
    print()

    # Get current date
    today = datetime.now()
    print(f"Date: {today.strftime('%Y-%m-%d %H:%M')}")
    print()

    # Step 1: Search for news
    articles = search_openai_frontier_news()

    if not articles:
        print("ERROR: No articles found. Exiting.")
        sys.exit(1)

    # Step 2: Analyze and rank
    top_stories = analyze_and_rank_stories(articles)

    if not top_stories:
        print("ERROR: No relevant stories found. Exiting.")
        sys.exit(1)

    # Step 3: Generate digest
    digest = generate_digest_markdown(top_stories, today)

    # Step 4: Save locally
    saved_path = save_digest_locally(digest, today)

    # Step 5: Send email
    recipient = config.RECIPIENT_EMAIL
    email_sent = send_email_via_sendgrid(digest, today, recipient)

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Stories found: {len(articles)}")
    print(f"Stories selected: {len(top_stories)}")
    print(f"Digest saved: {'Yes' if saved_path else 'No'}")
    print(f"Email sent: {'Yes' if email_sent else 'No'}")
    print()

    if email_sent:
        print(f"✅ Digest successfully sent to {recipient}")
    else:
        print(f"⚠️  Digest saved locally but email failed")
        if saved_path:
            print(f"   View digest at: {saved_path}")

    print("=" * 60)


if __name__ == "__main__":
    main()
