import os
import json
from pathlib import Path
from typing import Dict, List

# Core settings
MAX_RESULTS = 50
LABEL_PREFIX = "Auto/"
LOG_FILE = "logs/organizer.log"

# Path configuration
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"

# List configuration files
LIST_FILES = {
    "user": CONFIG_DIR / "userlist.json",
    "blocked": CONFIG_DIR / "blockedlist.json",
    "promotion": CONFIG_DIR / "promotionlist.json"
}

def load_list_config(file_path: Path) -> Dict[str, List[str]]:
    """Load a list configuration file with error handling"""
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
            # Validate structure
            if not all(key in config for key in ['domains', 'emails']):
                raise ValueError(f"Invalid structure in {file_path.name}")
            return config
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading {file_path.name}: {e}")
        return {"domains": [], "emails": []}

# Load all lists
USER_LIST = load_list_config(LIST_FILES["user"])
BLOCKED_LIST = load_list_config(LIST_FILES["blocked"])
PROMOTION_LIST = load_list_config(LIST_FILES["promotion"])