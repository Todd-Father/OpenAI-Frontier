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

# Search configuration - Focus on TECHNICAL VIDEO tutorials
# More specific queries to avoid irrelevant content
SEARCH_QUERIES = [
    # Access Control & Identity - Technical focus
    'OIDC OpenID Connect authentication tutorial',
    'OAuth 2.0 authorization flow explained',
    'Microsoft Entra ID conditional access tutorial',
    'multi-factor authentication MFA implementation',
    'RBAC role-based access control cloud',
    # Cloud Platform Security - Specific platforms
    'AWS IAM roles policies tutorial',
    'AWS IAM cross-account access',
    'Confluent Cloud security RBAC',
    'Databricks Unity Catalog access control',
    'Azure AD enterprise integration',
    # Data Security - Technical implementations
    'cloud data encryption key management',
    'secrets management vault tutorial',
    'zero trust security architecture'
]

# Authoritative video sources - Priority channels for security training
# These channels get bonus points in the ranking algorithm
PRIORITY_CHANNELS = [
    # Microsoft Official - High Priority
    'microsoft security',
    'microsoft mechanics',
    'microsoft azure',
    'microsoft 365',
    'azure',
    # AWS Official - High Priority
    'aws',
    'amazon web services',
    'aws online tech talks',
    # Security Training Platforms - High Priority
    'pluralsight',
    'linkedin learning',
    'udemy',
    'coursera',
    # Vendor Channels - Medium Priority
    'confluent',
    'databricks',
    'okta',
    'auth0',
    # Tech Education - Medium Priority
    'freecodeccamp',
    'techworld with nana',
    'cloud academy',
    # Security Experts - Medium Priority
    'networkchuck',
    'david bombal',
    'john hammond'
]

# Channels/keywords to EXCLUDE - Filter out non-technical content
EXCLUDED_KEYWORDS = [
    'interview',
    'career',
    'resume',
    'job',
    'salary',
    'certification exam',
    'study tips',
    'motivational',
    'lifestyle',
    'vlog',
    'reaction',
    'unboxing'
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
