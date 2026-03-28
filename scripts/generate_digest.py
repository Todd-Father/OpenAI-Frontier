#!/usr/bin/env python3
"""
Security Skills Training Digest Generator

Searches for security training videos, filters by duration, ranks by quality,
and sends curated digest via email 3x per week (Fri/Sat/Sun).
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from pathlib import Path
import requests
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import isodate  # For parsing ISO 8601 duration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import configuration
import config


def validate_config():
    """Validate required configuration variables."""
    try:
        if not hasattr(config, 'SEARCH_QUERIES'):
            logger.error("Missing SEARCH_QUERIES in config")
            return False
        logger.info("Configuration validated successfully")
        return True
    except AttributeError as e:
        logger.error(f"Configuration validation failed: {e}")
        return False


def search_training_videos():
    """
    Search for security training videos on YouTube.

    Returns list of videos with title, URL, duration, channel, and description.
    """
    logger.info("Searching for security training videos...")

    videos = []
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')

    if youtube_api_key:
        videos.extend(_search_youtube(youtube_api_key))
    else:
        logger.warning("YOUTUBE_API_KEY not configured, using fallback")
        videos = _get_fallback_videos()

    logger.info(f"Found {len(videos)} videos")
    return videos


def _search_youtube(api_key):
    """Search YouTube Data API for training videos."""
    videos = []
    base_url = "https://www.googleapis.com/youtube/v3/search"

    for query in config.SEARCH_QUERIES:
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'videoDuration': 'medium',  # 4-20 minutes
            'relevanceLanguage': 'en',
            'order': 'relevance',
            'maxResults': 5,
            'key': api_key
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Get video IDs to fetch duration
            video_ids = [item['id']['videoId'] for item in data.get('items', [])]

            if video_ids:
                # Fetch video details including duration
                video_details = _get_video_details(api_key, video_ids)
                videos.extend(video_details)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching YouTube for '{query}': {e}")
            continue

    return videos


def _get_video_details(api_key, video_ids):
    """Get detailed information about videos including duration."""
    details_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': ','.join(video_ids),
        'key': api_key
    }

    try:
        response = requests.get(details_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get('items', []):
            # Parse ISO 8601 duration (PT15M33S format)
            duration_iso = item['contentDetails']['duration']
            duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds())
            duration_minutes = duration_seconds // 60

            # Filter out very short videos (less than 5 minutes)
            # These are usually not substantial tutorials
            if duration_minutes < 5:
                logger.debug(f"Skipping short video ({duration_minutes}m): {item['snippet']['title'][:50]}")
                continue

            # Filter out very long videos (over 45 minutes)
            # These are usually full courses, not focused tutorials
            if duration_minutes > 45:
                logger.debug(f"Skipping long video ({duration_minutes}m): {item['snippet']['title'][:50]}")
                continue

            video = {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={item['id']}",
                'channel': item['snippet']['channelTitle'],
                'description': item['snippet']['description'][:200],  # First 200 chars
                'published_at': item['snippet']['publishedAt'],
                'duration_minutes': duration_minutes,
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'thumbnail': item['snippet']['thumbnails']['medium']['url']
            }
            videos.append(video)

        return videos

    except Exception as e:
        logger.error(f"Error fetching video details: {e}")
        return []


def _get_fallback_videos():
    """Fallback when YouTube API is not configured."""
    return [{
        'title': 'YouTube API Configuration Required',
        'url': 'https://console.cloud.google.com/apis/library/youtube.googleapis.com',
        'channel': 'System',
        'description': 'To receive real-time video curation, configure YOUTUBE_API_KEY. Get a free API key from Google Cloud Console.',
        'published_at': datetime.now().isoformat(),
        'duration_minutes': 0,
        'view_count': 0,
        'like_count': 0,
        'thumbnail': ''
    }]


def analyze_and_rank_videos(videos):
    """
    Analyze and rank videos by quality and relevance.

    Scoring criteria:
    - Duration preference: 5-15 min (+10), 15-20 min (+5), 20-30 min (+3)
    - View count: High views (+5)
    - Like ratio: Good engagement (+5)
    - Recency: Recent videos (+3)
    - Channel authority: Priority channels (+8)
    - Content filtering: Exclude irrelevant keywords

    Returns 2-4 videos, with max ONE video over 20 minutes.
    """
    logger.info(f"Analyzing and ranking {len(videos)} videos...")

    # Step 1: Remove duplicates by video URL/ID
    seen_urls = set()
    unique_videos = []
    for video in videos:
        url = video.get('url', '')
        if url not in seen_urls:
            seen_urls.add(url)
            unique_videos.append(video)
        else:
            logger.info(f"Removed duplicate: {video.get('title', 'Unknown')[:50]}")

    logger.info(f"After deduplication: {len(unique_videos)} unique videos")

    # Step 2: Filter out irrelevant content by excluded keywords
    filtered_videos = []
    for video in unique_videos:
        title = video.get('title', '').lower()
        description = video.get('description', '').lower()

        # Check if video contains excluded keywords
        has_excluded = False
        for keyword in config.EXCLUDED_KEYWORDS:
            if keyword.lower() in title or keyword.lower() in description:
                logger.info(f"Filtered out (excluded keyword '{keyword}'): {video.get('title', 'Unknown')[:50]}")
                has_excluded = True
                break

        if not has_excluded:
            filtered_videos.append(video)

    logger.info(f"After filtering: {len(filtered_videos)} relevant videos")

    # Step 3: Score and rank videos
    scored_videos = []

    for video in filtered_videos:
        score = 0
        duration = video['duration_minutes']

        # Duration scoring - prefer 5-15 min
        if 5 <= duration <= 15:
            score += 10
        elif 15 < duration <= 20:
            score += 5
        elif 20 < duration <= 30:
            score += 3
        elif duration < 5:
            score += 2  # Too short
        else:
            score -= 5  # Too long (over 30 min)

        # View count scoring
        views = video.get('view_count', 0)
        if views > 100000:
            score += 5
        elif views > 10000:
            score += 3

        # Engagement scoring (like ratio)
        likes = video.get('like_count', 0)
        if views > 0 and likes > 0:
            like_ratio = likes / views
            if like_ratio > 0.05:  # 5%+ like ratio is good
                score += 5
            elif like_ratio > 0.02:
                score += 3

        # Recency scoring
        try:
            published = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
            days_old = (datetime.now(published.tzinfo) - published).days
            if days_old < 180:  # Within 6 months
                score += 3
            elif days_old < 365:  # Within 1 year
                score += 1
        except:
            pass

        # Priority channel scoring (improved)
        channel = video.get('channel', '').lower()
        for priority_channel in config.PRIORITY_CHANNELS:
            if priority_channel.lower() in channel:
                score += 8  # Higher bonus for priority channels
                logger.debug(f"Priority channel bonus for: {channel}")
                break

        scored_videos.append({
            'video': video,
            'score': score
        })

    # Sort by score
    scored_videos.sort(key=lambda x: x['score'], reverse=True)

    # Step 4: Select top videos with diversity
    selected = []
    selected_video_ids = set()
    long_video_count = 0

    for item in scored_videos:
        if len(selected) >= config.MAX_VIDEOS:
            break

        video = item['video']
        video_url = video.get('url', '')
        duration = video['duration_minutes']

        # Skip if already selected (extra safety check)
        if video_url in selected_video_ids:
            continue

        # Check if this is a long video (20+ min)
        if duration > 20:
            if long_video_count >= 1:
                continue  # Skip, already have one long video
            long_video_count += 1

        selected.append(video)
        selected_video_ids.add(video_url)

    # Ensure we have at least MIN_VIDEOS
    if len(selected) < config.MIN_VIDEOS:
        # Add more videos regardless of duration rules
        for item in scored_videos:
            video = item['video']
            video_url = video.get('url', '')
            if video_url not in selected_video_ids and len(selected) < config.MIN_VIDEOS:
                selected.append(video)
                selected_video_ids.add(video_url)

    logger.info(f"Selected {len(selected)} videos for digest")
    return selected


def generate_digest_markdown(videos, date):
    """Generate formatted markdown digest for video content."""
    logger.info(f"Generating digest for {len(videos)} videos...")

    date_str = date.strftime('%B %d, %Y')
    day_of_week = date.strftime('%A')

    digest = f"""# 🎓 Security Skills Training Digest
**{day_of_week}, {date_str}**

---

## Today's Training Videos

"""

    for i, video in enumerate(videos, 1):
        title = video['title']
        url = video['url']
        channel = video['channel']
        duration = video['duration_minutes']
        description = video.get('description', 'No description available')

        # Duration badge
        if duration <= 10:
            duration_badge = "⚡ Quick ({}m)".format(duration)
        elif duration <= 20:
            duration_badge = "📺 Standard ({}m)".format(duration)
        else:
            duration_badge = "🎬 Deep Dive ({}m)".format(duration)

        digest += f"""### {i}. {title}

**Channel:** {channel} | {duration_badge}

**Watch:** [{url}]({url})

**Overview:** {description}

**Why This Matters:** Build foundational skills in access control and identity management that directly apply to AWS, Confluent Cloud, and Databricks integration scenarios.

---

"""

    # Add learning tips
    digest += f"""
## 💡 Learning Tips

- **Take Notes:** Key concepts, commands, and configurations
- **Hands-on Practice:** Try examples in your own AWS/Azure environment
- **Connect the Dots:** Think about how this applies to your Confluent/Databricks work
- **Pace Yourself:** Don't rush - mastery comes from practice

---

## 📚 This Week's Focus

Building towards RBAC role design for multi-cloud integration:
- Week 1-2: Authentication & Authorization fundamentals
- Week 3-4: OIDC/OAuth flows and Entra ID configuration
- Week 5-6: Practical RBAC for AWS ↔ Confluent Cloud
- Week 7-8: Advanced: Just-in-time access & Zero Trust

---

*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M UTC')}*

**Next Digest:** See you next session! 🚀
"""

    return digest


def save_digest_locally(digest, date):
    """Save digest to local training-digests/ folder."""
    logger.info("Saving digest locally...")

    digest_folder = Path(config.DIGEST_FOLDER)
    digest_folder.mkdir(exist_ok=True)

    filename = f"{date.strftime('%Y-%m-%d')}.md"
    filepath = digest_folder / filename

    try:
        filepath.write_text(digest, encoding='utf-8')
        logger.info(f"Digest saved to: {filepath}")
        return str(filepath)
    except Exception as e:
        logger.error(f"Error saving digest: {e}")
        return None


def send_email_via_sendgrid(digest, date, recipient):
    """Send digest email via SendGrid."""
    logger.info(f"Sending email to {recipient}...")

    api_key = config.SENDGRID_API_KEY
    if not api_key:
        logger.error("SENDGRID_API_KEY not set. Email not sent.")
        return False

    # Create HTML version
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.7;
                color: #1a1a1a;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
            }}
            h1 {{
                color: #2563eb;
                border-bottom: 3px solid #2563eb;
                padding-bottom: 10px;
                font-size: 28px;
            }}
            h2 {{
                color: #2c3e50;
                margin-top: 30px;
                font-size: 22px;
                font-weight: 600;
            }}
            h3 {{
                color: #000000;
                font-size: 18px;
                font-weight: 600;
                margin-top: 20px;
            }}
            p {{
                color: #2c3e50;
                margin: 10px 0;
            }}
            strong {{
                color: #1a1a1a;
                font-weight: 600;
            }}
            a {{
                color: #0066cc;
                text-decoration: none;
                font-weight: 500;
            }}
            a:hover {{
                text-decoration: underline;
                color: #004499;
            }}
            .video-card {{
                background: #f9f9f9;
                border-left: 4px solid #2563eb;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
            .badge {{
                background: #e8f4f8;
                color: #2c3e50;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 0.9em;
                font-weight: 600;
            }}
            hr {{
                border: none;
                border-top: 1px solid #e0e0e0;
                margin: 25px 0;
            }}
        </style>
    </head>
    <body>
        <div>{digest.replace('### ', '<h3>').replace('## ', '<h2>').replace('# ', '<h1>')}</div>
    </body>
    </html>
    """

    subject = config.EMAIL_SUBJECT_TEMPLATE.format(date=date.strftime('%A, %B %d'))

    message = Mail(
        from_email=config.SENDER_EMAIL,
        to_emails=recipient,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        logger.info(f"Email sent successfully! Status code: {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False


def main():
    """Main execution function."""
    logger.info("=" * 60)
    logger.info("Security Skills Training Digest Generator")
    logger.info("=" * 60)

    today = datetime.now()
    logger.info(f"Date: {today.strftime('%Y-%m-%d %H:%M')}")

    # Validate configuration
    if not validate_config():
        logger.error("Configuration validation failed. Exiting.")
        sys.exit(1)

    # Step 1: Search for training videos
    videos = search_training_videos()

    if not videos:
        logger.error("No videos found. Exiting.")
        sys.exit(1)

    # Step 2: Analyze and rank
    top_videos = analyze_and_rank_videos(videos)

    if not top_videos:
        logger.error("No relevant videos found. Exiting.")
        sys.exit(1)

    # Step 3: Generate digest
    digest = generate_digest_markdown(top_videos, today)

    # Step 4: Save locally
    saved_path = save_digest_locally(digest, today)

    # Step 5: Send email
    recipient = config.RECIPIENT_EMAIL
    email_sent = send_email_via_sendgrid(digest, today, recipient)

    # Summary
    logger.info("=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Videos found: {len(videos)}")
    logger.info(f"Videos selected: {len(top_videos)}")
    logger.info(f"Digest saved: {'Yes' if saved_path else 'No'}")
    logger.info(f"Email sent: {'Yes' if email_sent else 'No'}")

    if email_sent:
        logger.info(f"✅ Training digest successfully sent to {recipient}")
    else:
        logger.warning(f"⚠️  Digest saved locally but email failed")
        if saved_path:
            logger.info(f"   View digest at: {saved_path}")

    logger.info("=" * 60)


if __name__ == "__main__":
    main()
