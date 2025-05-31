import os
import logging
from typing import Optional  # Add this import
from googleapiclient.discovery import build
from src.utils.email_utils import (
    get_sender_email,
    classify_email,
    extract_email_body
)
from src.config.settings import MAX_RESULTS, LABEL_PREFIX

logger = logging.getLogger(__name__)

class EmailProcessor:
    def __init__(self, service, base_dir):
        self.service = service
        self.base_dir = base_dir
        self._ensure_system_labels_exist()

    def _ensure_system_labels_exist(self):
        """Create system labels if they don't exist"""
        for label_name in ["Blocked", "Promotion"]:
            self.create_label(label_name, is_system_label=True)

    def create_label(self, label_name: str, is_system_label: bool = False) -> Optional[str]:
        """Create a label if it doesn't exist"""
        full_name = label_name if is_system_label else f"{LABEL_PREFIX}{label_name}"
        
        labels = self.service.users().labels().list(userId='me').execute().get('labels', [])
        
        # Check if label exists
        existing = next(
            (label for label in labels if label['name'].lower() == full_name.lower()),
            None
        )
        if existing:
            return existing['id']
        
        # Create new label
        try:
            label = self.service.users().labels().create(
                userId='me',
                body={
                    'name': full_name,
                    'labelListVisibility': 'labelShow',
                    'messageListVisibility': 'show'
                }
            ).execute()
            logger.info(f"Created label: {full_name}")
            return label['id']
        except Exception as e:
            logger.error(f"Failed to create label {full_name}: {e}")
            return None

    def process_emails(self) -> int:
        """Process emails from inbox and categorize them"""
        try:
            # Retrieve messages
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                maxResults=MAX_RESULTS
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                logger.info("No new messages in inbox")
                return 0
                
            processed = 0
            for msg in messages:
                full_msg = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()
                
                # Extract headers
                headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}
                sender = headers.get('From', '')
                
                if not sender:
                    continue
                
                # Classify email
                label_name = classify_email(sender)
                
                # Only process if classification exists
                if label_name:
                    label_id = self.create_label(
                        label_name,
                        is_system_label=label_name in ["Blocked", "Promotion"]
                    )
                    
                    if label_id:
                        self.service.users().messages().modify(
                            userId='me',
                            id=msg['id'],
                            body={
                                'addLabelIds': [label_id],
                                'removeLabelIds': ['INBOX']  # Move out of inbox
                            }
                        ).execute()
                        processed += 1
                        logger.debug(f"Labeled email from {sender} as {label_name}")
            
            logger.info(f"Processed {processed} emails")
            return processed
            
        except Exception as e:
            logger.exception(f"Email processing failed: {e}")
            return 0