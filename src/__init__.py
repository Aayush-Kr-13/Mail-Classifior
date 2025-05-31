# src/__init__.py
from .auth import authenticate_gmail
from .email_processor import EmailProcessor
from .config import MAX_RESULTS, LABEL_PREFIX

__all__ = [
    'authenticate_gmail',
    'EmailProcessor',
    'MAX_RESULTS',
    'LABEL_PREFIX'
]

__version__ = "1.0.0"