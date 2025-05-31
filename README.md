# Gmail Organizer

Automatically categorizes your Gmail emails into predefined categories.

## Features

- 🔒 Secure OAuth 2.0 authentication
- 📧 Processes up to 50 emails per execution
- 🏷️ Categorizes emails into 3 label types:
  - `Promotion` - For marketing/commercial emails
  - `Blocked` - For unwanted/spam emails
  - `From_[username]` - For personal emails (e.g., `From_john`)
- 📂 Leaves uncategorized emails in the inbox
- 📊 Detailed logging of all operations
- ⚙️ Configurable through JSON configuration files

## Configuration Files

The system uses these JSON files in `config/` directory:

1. `promotionlist.json` - Domains/emails to mark as promotions
   ```json
   {
       "domains": ["amazon.com", "netflix.com"],
       "emails": ["newsletter@store.com"]
   }

2. `blockedlist.json` - Domains/emails to block

    ```json
    {
        "domains": ["spam.org"],
        "emails": ["unwanted@sender.com"]
    }

3. `userlist.json` - Personal contacts to label by username

    ```json
    {
        "domains": ["gmail.com"],
        "emails": ["important@client.com"]
    }

## How Classification Works

1. `Blocked` → Checks blockedlist.json first

2. `Promotion` → Then checks promotionlist.json

3. `Personal` → Finally checks userlist.json

4. `Uncategorized` → Remains in inbox if no match found

## Example Workflow

1. `Email from news@amazon.com` → Promotion label

2. `Email from spam@spam.org` → Blocked label

3. `Email from john@gmail.com` → From_john label

4. `Email from unknown@domain.com` → Stays in inbox


# How to Run Gmail Organizer

Follow these steps to set up and run the Gmail Organizer:

## Set Up Credentials

1. Create a `data/` folder in your project directory.
2. Place your downloaded `credentials.json` file inside the `data/` folder.

## Install Dependencies

Install the required Python packages using pip:

    pip install -r requirements.txt

## Command to Execute

Use the following command to run the main script:

    python -m src.main

# First-Time Setup

When you run the script for the first time:

- A browser window will automatically open for Google OAuth login.
- Sign in with your Google account and approve the required permissions.
- After successful authentication, a `token.pickle` file will be generated to securely store your access token for future use.

# Expected Output

- Emails will be processed and categorized based on the rules defined in your configuration files (`promotionlist.json`, `blockedlist.json`, `userlist.json`).
- The terminal will display log output indicating which emails were labeled, skipped, or left in the inbox.
