#!/usr/bin/env python3
"""
EDA Daily Digest Generator
import html

This script searches for event driven architecture news, analyzes and ranks stories,
generates a digest, saves it locally, and emails it via SendGrid.
"""
# Additional code for sanitizing html_content

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
# Example of sanitizing html_content
html_content = html.escape(html_content)  # Sanitize to prevent HTML injection

# Load environment variables from .env file (for local testing)
load_dotenv()

# Import configuration
import config


def search_EDA_news():
    """
    Search for recent event driven architecture news articles specifcally around security related to confluent cloud, kafka api, flink and kong.

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
    - Mentions "Event Driven Architecture Security" explicitly (+10)
    - From authoritative source (+5)
    - Recent (past 24h: +5, past 48h: +3)
    - Long content (+3)
    - Contains keywords: enterprise, EDA, security, Confluent Cloud, Kafka  (+2 each)

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

        # Check for "Event Driven Architecture" mention (high priority)
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
