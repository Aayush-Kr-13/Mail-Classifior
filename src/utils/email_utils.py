import re
import base64
from typing import Dict, Any, List, Optional  
from src.config.settings import USER_LIST, BLOCKED_LIST, PROMOTION_LIST

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

def classify_email(sender: str) -> Optional[str]:
    """
    Classify email based on lists
    Returns: None (keep in inbox) or label name
    """
    email = get_sender_email(sender)
    domain = get_sender_domain(sender)
    
    # Check blocked list first
    if (domain in BLOCKED_LIST["domains"] or 
        email in BLOCKED_LIST["emails"]):
        return "Blocked"
    
    # Check promotion list
    if (domain in PROMOTION_LIST["domains"] or 
        email in PROMOTION_LIST["emails"]):
        return "Promotion"
    
    # Check user list
    if (domain in USER_LIST["domains"] or 
        email in USER_LIST["emails"]):
        username = email.split('@')[0]
        return f"From_{username}"
    
    # Not in any list - keep in inbox
    return None

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