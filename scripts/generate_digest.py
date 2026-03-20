#!/usr/bin/env python3
"""
EDA Daily Digest Generator

This script searches for event driven architecture news, analyzes and ranks stories,
generates a digest, saves it locally, and emails it via SendGrid.
"""

import os
import sys
import html
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

def search_EDA_news():
    """
    Search for recent event driven architecture news articles specifically around security related to confluent cloud, kafka api, flink and kong.

    Uses web search to find articles from the past 24-48 hours.
    Returns list of articles with title, URL, source, date, and snippet.
    """
    print("Searching for event driven architecture news...")

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
        'description': 'To receive real-time Event Driven Architecture news, please configure NewsAPI. See SETUP.md for instructions.',
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
    - Contains keywords: enterprise, EDA, security, Confluent Cloud, Kafka (+2 each)

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
                now = datetime.now(pub_date.tzinfo) if pub_date.tzinfo else datetime.now()
                hours_old = (now - pub_date).total_seconds() / 3600

                if hours_old <= 24:
                    score += 5
                elif hours_old <= 48:
                    score += 3
            except (ValueError, TypeError):
                pass

        # Check content length
        if len(content) > 500:
            score += 3

        # Check for keywords
        keywords = ['enterprise', 'eda', 'security', 'confluent', 'kafka', 'event-driven']
        for keyword in keywords:
            if keyword in full_text:
                score += 2

        scored_articles.append({
            'article': article,
            'score': score
        })

    # Sort by score and return top articles
    scored_articles.sort(key=lambda x: x['score'], reverse=True)
    top_articles = scored_articles[:config.MAX_STORIES] if hasattr(config, 'MAX_STORIES') else scored_articles[:10]

    return [item['article'] for item in top_articles]

def _extract_domain(url):
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return ''

def generate_digest_html(articles):
    """
    Generate HTML digest from articles.
    
    Sanitizes content to prevent HTML injection.
    """
    if not articles:
        return '<p>No articles found.</p>'

    html_content = '<h1>Event Driven Architecture Digest</h1>'
    html_content += f'<p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>'
    html_content += '<ul>'

    for article in articles:
        title = html.escape(article.get('title', 'No title'))
        url = html.escape(article.get('url', ''))
        source = html.escape(article.get('source', 'Unknown'))
        description = html.escape(article.get('description', ''))

        html_content += f'<li><a href="{url}">{title}</a> ({source})<br/>{description}</li>'

    html_content += '</ul>'
    
    return html_content

def send_digest_email(digest_html, recipient_email):
    """
    Send digest via SendGrid email.
    """
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        message = Mail(
            from_email=os.getenv('FROM_EMAIL'),
            to_emails=recipient_email,
            subject='Event Driven Architecture Daily Digest',
            html_content=digest_html
        )
        response = sg.send(message)
        print(f"Email sent successfully. Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == '__main__':
    articles = search_EDA_news()
    ranked_articles = analyze_and_rank_stories(articles)
    digest_html = generate_digest_html(ranked_articles)
    
    # Save locally
    with open('digest.html', 'w') as f:
        f.write(digest_html)
    print("Digest saved to digest.html")
    
    # Send email if configured
    recipient = os.getenv('DIGEST_RECIPIENT_EMAIL')
    if recipient:
        send_digest_email(digest_html, recipient)
