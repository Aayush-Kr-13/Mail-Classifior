import json
from pathlib import Path
from typing import Dict, List

# Core settings
MAX_RESULTS = 50
LABEL_PREFIX = "Auto/"
LOG_FILE = "logs/organizer.log"

# Path configuration
BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "config" / "email_categories.json"

def load_categories() -> Dict[str, Dict[str, List[str]]]:
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

            # Validate structure
            required_sections = {'blocked', 'promotion', 'user'}
            if not required_sections.issubset(config.keys()):
                raise ValueError("Missing required sections")

            # Validate each section has 'domains' and 'emails'
            for section in required_sections:
                if not all(k in config[section] for k in ['domains', 'emails']):
                    raise ValueError(f"Invalid structure in section: {section}")

            return config

    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        raise RuntimeError(f"Failed to load email categories: {str(e)}")

EMAIL_CATEGORIES = load_categories()

# Extracted categories
USER_LIST = EMAIL_CATEGORIES['user']
BLOCKED_LIST = EMAIL_CATEGORIES['blocked']
PROMOTION_LIST = EMAIL_CATEGORIES['promotion']
