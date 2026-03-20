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
    'event driven architecture updates',
    'event driven architecture patterns'
]

# Authoritative sources (higher priority)
AUTHORITATIVE_SOURCES = [
    'openai.com',
    'techcrunch.com',
    'theverge.com',
    'arstechnica.com',
    'wired.com',
    'forbes.com',
    'reuters.com',
    'bloomberg.com',
    'venturebeat.com',
    'zdnet.com',
    'microsoft.com',
    'cnbc.com',
    'fortune.com'
]

# Story limits
MIN_STORIES = 3
MAX_STORIES = 7

# Local storage
DIGEST_FOLDER = 'daily-digests'

# Email template configuration
EMAIL_SUBJECT_TEMPLATE = "Event Driven Architecture Daily Digest - {date}"
