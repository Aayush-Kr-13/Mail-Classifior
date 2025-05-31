from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.auth import authenticate_gmail
from src.email_processor import EmailProcessor
from src.utils.file_utils import setup_logging
import logging
import sys
import os

def main():
    """Main entry point for the Gmail Organizer application."""
    setup_logging()
    logger = logging.getLogger(__name__)

    # Set the base directory for storing emails
    base_dir = os.path.join(os.getcwd(), "emails_by_label")

    try:
        logger.info("Starting Gmail Organizer")

        # Authenticate and build service
        logger.debug("Authenticating with Gmail API")
        creds = authenticate_gmail()
        service = build('gmail', 'v1', credentials=creds)

        # Process emails
        logger.debug("Initializing email processor")
        processor = EmailProcessor(service, base_dir)

        logger.info("Starting email processing")
        processed = processor.process_emails()

        logger.info(f"Successfully processed {processed} emails")
        sys.exit(0)  # Success exit code

    except HttpError as he:
        logger.error(f"Gmail API error: {he}")
        if he.resp.status == 403:
            logger.error("Insufficient permissions. Check your OAuth scopes.")
        sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(130)  # Standard exit code for Ctrl+C

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)  # Generic error exit code

if __name__ == "__main__":
    main()