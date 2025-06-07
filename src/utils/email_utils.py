import re
import base64
from typing import Dict, Any, Optional
from src.config.settings import EMAIL_CATEGORIES

def get_sender_email(sender_header: str) -> str:
    """Extract clean email address from From header"""
    if not sender_header:
        return ""
    
    # Handle "Name <email@domain.com>" format
    if '<' in sender_header:
        match = re.search(r'<(.+?)>', sender_header)
        if match:
            return match.group(1).lower()
    return sender_header.lower()

def get_sender_domain(email_address: str) -> str:
    """Extract domain from email address"""
    email = get_sender_email(email_address)
    if '@' in email:
        return email.split('@')[-1]
    return "unknown"

def extract_meeting_links(body: str) -> Optional[str]:
    """Extract meeting links from email body"""
    patterns = EMAIL_CATEGORIES.get('meeting', {}).get('patterns', [])
    combined_pattern = "|".join(f"({pattern})" for pattern in patterns)
    
    if re.search(combined_pattern, body):
        return "Meeting"
    return None

def classify_email(sender: str, body: str) -> Optional[list[str]]:
    """
    Classify email based on EMAIL_CATEGORIES and body content.
    Returns: list of label names (can be multiple), or None
    """
    labels = []
    email = get_sender_email(sender)
    domain = get_sender_domain(email)
    categories = EMAIL_CATEGORIES

    # Check blocked
    if domain in categories["blocked"]["domains"] or email in categories["blocked"]["emails"]:
        labels.append("Blocked")
    # Check promotion
    if domain in categories["promotion"]["domains"] or email in categories["promotion"]["emails"]:
        labels.append("Promotion")
    # Check user
    if domain in categories["user"]["domains"] or email in categories["user"]["emails"]:
        labels.append(f"From_{email.split('@')[0]}")
    # Check meeting links in email body
    meeting_label = extract_meeting_links(body)
    if meeting_label:
        labels.append(meeting_label)

    return labels if labels else None

def extract_email_body(payload: Dict[str, Any]) -> str:
    """Extract and decode email body text"""
    def decode_body(data: str) -> str:
        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    
    # Handle multipart emails
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                return decode_body(part['body'].get('data', ''))
    
    # Handle simple emails
    if 'body' in payload:
        return decode_body(payload['body'].get('data', ''))
    
    return ""
