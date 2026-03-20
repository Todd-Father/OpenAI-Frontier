#!/usr/bin/env python3
"""
EDA Daily Digest Generator

This script searches for event driven architecture news, analyzes and ranks stories,
generates a digest, saves it locally, and emails it via SendGrid.
"""

import os
import sys
import html
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
import markdown

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file (for local testing)
load_dotenv()

# Import configuration
import config


def validate_config():
    """Validate required configuration variables."""
    try:
        if not hasattr(config, 'SEARCH_QUERIES'):
            logger.error("Missing SEARCH_QUERIES in config")
            return False
        if not hasattr(config, 'AUTHORITATIVE_SOURCES'):
            logger.error("Missing AUTHORITATIVE_SOURCES in config")
            return False
        logger.info("Configuration validated successfully")
        return True
    except AttributeError as e:
        logger.error(f"Configuration validation failed: {e}")
        return False


def search_EDA_news():
    """
    Search for recent event driven architecture news articles specifically around security related to confluent cloud, kafka api, flink and kong.

    Uses web search to find articles from the past 24-48 hours.
    Returns list of articles with title, URL, source, date, and snippet.
    """
    logger.info("Searching for event driven architecture news...")

    articles = []

    # Method 1: Use NewsAPI (requires API key)
    newsapi_key = os.getenv('NEWSAPI_KEY')
    if newsapi_key:
        articles.extend(_search_newsapi(newsapi_key))
    else:
        logger.warning("NEWSAPI_KEY not configured in environment variables")

    # Method 2: Manual RSS/scraping fallback (add your preferred sources)
    # This is a fallback if NewsAPI is not configured
    if not articles:
        logger.warning("No news API configured. Using fallback method...")
        articles = _get_fallback_articles()

    logger.info(f"Found {len(articles)} articles")
    return articles


def _search_newsapi(api_key):
    """Search using NewsAPI"""
    articles = []

    # Calculate date range (past 2 days to catch more stories)
    to_date = datetime.now(timezone.utc)
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
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error searching NewsAPI for '{query}': {e}")
            continue
        except ValueError as e:
            logger.error(f"JSON parsing error for '{query}': {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error searching NewsAPI for '{query}': {e}", exc_info=True)
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
        'published_at': datetime.now(timezone.utc).isoformat(),
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
    logger.info(f"Analyzing and ranking {len(articles)} articles...")

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
        try:
            authoritative_sources = getattr(config, 'AUTHORITATIVE_SOURCES', [])
            if any(auth_source in source_domain for auth_source in authoritative_sources):
                score += 5
        except (TypeError, AttributeError) as e:
            logger.debug(f"Error checking authoritative sources: {e}")

        # Check recency
        published_at = article.get('published_at', '')
        if published_at:
            try:
                pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                hours_old = (now - pub_date).total_seconds() / 3600

                if hours_old <= 24:
                    score += 5
                elif hours_old <= 48:
                    score += 3
            except ValueError as e:
                logger.debug(f"Could not parse date '{published_at}': {e}")
            except TypeError as e:
                logger.debug(f"Type error processing date '{published_at}': {e}")

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
    max_stories = getattr(config, 'MAX_STORIES', 10)
    top_articles = scored_articles[:max_stories]

    return [item['article'] for item in top_articles]


def _extract_domain(url):
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except (ValueError, AttributeError) as e:
        logger.debug(f"Could not extract domain from URL '{url}': {e}")
        return ''
    except Exception as e:
        logger.error(f"Unexpected error extracting domain from '{url}': {e}", exc_info=True)
        return ''


def generate_digest_html(articles):
    """
    Generate HTML digest from articles.
    
    Sanitizes content to prevent HTML injection.
    """
    if not articles:
        return '<p>No articles found.</p>'

    html_parts = [
        '<h1>Event Driven Architecture Digest</h1>',
        f'<p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>',
        '<ul>'
    ]

    for article in articles:
        title = html.escape(article.get('title', 'No title'))
        url = html.escape(article.get('url', ''))
        source = html.escape(article.get('source', 'Unknown'))
        description = html.escape(article.get('description', ''))

        html_parts.append(
            f'<li><a href="{url}">{title}</a> ({source})<br/>{description}</li>'
        )

    html_parts.append('</ul>')
    
    return '\n'.join(html_parts)


def send_digest_email(digest_html, recipient_email):
    """
    Send digest via SendGrid email.
    """
    # Validate environment variables
    api_key = os.getenv('SENDGRID_API_KEY')
    from_email = os.getenv('SENDER_EMAIL')

    if not api_key:
        logger.error("SENDGRID_API_KEY not configured in environment variables")
        return False
    if not from_email:
        logger.error("FROM_EMAIL not configured in environment variables")
        return False

    try:
        sg = SendGridAPIClient(api_key)
        message = Mail(
            from_email=from_email,
            to_emails=recipient_email,
            subject='Event Driven Architecture Daily Digest',
            html_content=digest_html
        )
        response = sg.send(message)
        logger.info(f"Email sent successfully to {recipient_email}. Status code: {response.status_code}")
        return True
    except KeyError as e:
        logger.error(f"Missing environment variable: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending email to {recipient_email}: {e}", exc_info=True)
        return False


if __name__ == '__main__':
    try:
        # Validate configuration
        if not validate_config():
            logger.error("Configuration validation failed. Exiting.")
            sys.exit(1)

        # Search for articles
        articles = search_EDA_news()
        if not articles:
            logger.warning("No articles found")
        
        # Analyze and rank articles
        ranked_articles = analyze_and_rank_stories(articles)
        logger.info(f"Ranked {len(ranked_articles)} articles")

        # Generate digest HTML
        digest_html = generate_digest_html(ranked_articles)
        
        # Save locally as markdown
        try:
            # Create daily-digests directory if it doesn't exist
            digest_folder = Path('daily-digests')
            digest_folder.mkdir(exist_ok=True)

            # Save as markdown with date in filename
            date_str = datetime.now().strftime('%Y-%m-%d')
            digest_path = digest_folder / f"{date_str}.md"

            # Convert HTML to markdown for storage
            digest_md = f"# Event Driven Architecture Daily Digest\n\n{digest_html}\n"

            with open(digest_path, 'w', encoding='utf-8') as f:
                f.write(digest_md)
            logger.info(f"Digest saved successfully to {digest_path}")
        except IOError as e:
            logger.error(f"Error writing digest file: {e}")
            sys.exit(1)
            
        # Send email if configured
        recipient = os.getenv('RECIPIENT_EMAIL')
        if recipient:
            logger.info(f"Sending digest to {recipient}")
            send_digest_email(digest_html, recipient)
        else:
            logger.info("RECIPIENT_EMAIL not configured, skipping email send")
            
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
