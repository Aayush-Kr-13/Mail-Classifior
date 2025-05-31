import os
import logging
from pathlib import Path
from typing import Optional
from src.config.settings import LOG_FILE

def setup_logging(log_file: Optional[str] = None) -> None:
    """
    Configure logging for the application.
    
    Args:
        log_file: Optional path to log file (defaults to settings.LOG_FILE)
    """
    log_path = Path(log_file or LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    logging.captureWarnings(True)

def ensure_directory_exists(path: str) -> None:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        path: Path to directory
    """
    Path(path).mkdir(parents=True, exist_ok=True)

def safe_write_file(path: str, content: str) -> bool:
    """
    Safely write content to a file with error handling.
    
    Args:
        path: File path
        content: Content to write
    
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logging.error(f"Failed to write file {path}: {e}")
        return False