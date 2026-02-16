"""
Configuration settings for OpenAI Frontier Daily Digest
"""
import os
from datetime import datetime

# Email configuration
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'tbeavers12@gmail.com')
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'digest@openai-frontier.com')
SENDER_NAME = 'OpenAI Frontier Digest'
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Search configuration
SEARCH_QUERIES = [
    'OpenAI Frontier news',
    'OpenAI Frontier enterprise',
    'OpenAI Frontier security',
    'OpenAI Frontier updates',
    'OpenAI Frontier partnership'
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
EMAIL_SUBJECT_TEMPLATE = "OpenAI Frontier Daily Digest - {date}"
