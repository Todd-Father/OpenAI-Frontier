"""
Configuration settings for OpenAI Frontier Daily Digest
"""
import os
from datetime import datetime

# Email configuration
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
if not RECIPIENT_EMAIL:
    raise ValueError("RECIPIENT_EMAIL environment variable not set")
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'digest@openai-frontier.com')
SENDER_NAME = 'Event Driven Architecture Digest'
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Search configuration
SEARCH_QUERIES = [
    'event driven architecture news',
    'event driven architecture enterprise',
    'event driven architecture security',
    'Kafka security news',
    'Confluent Cloud updates',
    'AWS EventBridge news',
    'Microsoft Entra ID updates',
    'Zero Trust Architecture news',
    'Flink security updates',
    'Kong API gateway news'
]

# Authoritative sources (higher priority)
AUTHORITATIVE_SOURCES = [
    # EDA-specific sources
    'confluent.io',
    'kafka.apache.org',
    'aws.amazon.com',
    'aws-blog',
    'konghq.com',
    'flink.apache.org',
    # Microsoft/Identity sources
    'microsoft.com',
    'learn.microsoft.com',
    'techcommunity.microsoft.com',
    # Security/ZTA sources
    'nist.gov',
    'csrc.nist.gov',
    # General tech news
    'techcrunch.com',
    'theverge.com',
    'arstechnica.com',
    'wired.com',
    'forbes.com',
    'reuters.com',
    'bloomberg.com',
    'venturebeat.com',
    'zdnet.com',
    'cnbc.com',
    'infoq.com',
    'thenewstack.io'
]

# Story limits
MIN_STORIES = 5
MAX_STORIES = 10

# Local storage
DIGEST_FOLDER = 'daily-digests'

# Email template configuration
EMAIL_SUBJECT_TEMPLATE = "Event Driven Architecture Daily Digest - {date}"
