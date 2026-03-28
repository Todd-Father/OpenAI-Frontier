"""
Configuration settings for Security Skills Training Digest
"""
import os
from datetime import datetime

# Email configuration
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
if not RECIPIENT_EMAIL:
    raise ValueError("RECIPIENT_EMAIL environment variable not set")
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'security-training@skills.com')
SENDER_NAME = 'Security Skills Training'
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Search configuration - Focus on VIDEO tutorials
SEARCH_QUERIES = [
    # Access Control & Identity
    'OIDC tutorial video',
    'OAuth 2.0 explained video',
    'Microsoft Entra ID tutorial',
    'MFA implementation video',
    'RBAC explained video',
    # Cloud Platform Security
    'AWS IAM roles tutorial',
    'Confluent Cloud security video',
    'Databricks access control tutorial',
    'Azure AD integration video',
    # Data Security
    'data encryption tutorial',
    'secrets management best practices video',
    'cloud data security video'
]

# Authoritative video sources (YouTube channels & platforms)
AUTHORITATIVE_SOURCES = [
    # Microsoft Official
    'youtube.com/microsoft',
    'learn.microsoft.com',
    'techcommunity.microsoft.com',
    # AWS Official
    'youtube.com/aws',
    'aws.amazon.com',
    # Security Training Platforms
    'youtube.com',
    'pluralsight.com',
    'linkedin.com/learning',
    'udemy.com',
    # Vendor Channels
    'confluent.io',
    'databricks.com',
    # Security Experts
    'youtube.com/c/NetworkChuck',
    'youtube.com/c/DavidBombal'
]

# Learning limits - Keep it manageable!
MIN_VIDEOS = 2
MAX_VIDEOS = 4

# Local storage
DIGEST_FOLDER = 'training-digests'

# Email template configuration
EMAIL_SUBJECT_TEMPLATE = "🎓 Security Skills Training - {date}"

# Progressive learning tracks
LEARNING_TRACKS = {
    'foundations': [
        'Authentication basics',
        'Authorization concepts',
        'Identity providers overview'
    ],
    'intermediate': [
        'OIDC and OAuth 2.0 flow',
        'Entra ID configuration',
        'RBAC role design'
    ],
    'advanced': [
        'Multi-cloud identity federation',
        'Just-in-time access',
        'Zero Trust implementation'
    ]
}
