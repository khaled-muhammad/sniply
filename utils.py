import json
import os
import pathlib
from groq import Groq
from datetime import datetime

from models import Account, AccountSettings

try:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
except Exception as e:
    print(f"Warning: Could not initialize Groq client: {e}")
    client = None

POST_CATEGORIES = [
    "news",
    "entertainment",
    "sports",
    "technology",
    "lifestyle",
    "personal",
    "advertisement",
    "meme",
    "other"
]

def getSMAPath():
    p = f"{os.path.expanduser('~/sniply')}/sm_accs/"
    pathlib.Path(p).mkdir(parents=True, exist_ok=True)

    return p

def saveAuth(platform_name, username, cookies):
    sm_dir_path = f"{getSMAPath()}/{platform_name}"
    pathlib.Path(sm_dir_path).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(sm_dir_path, f"{username}.sc"), 'w') as f:
        json.dump(cookies, f)

def getAccounts():
    smaPath = getSMAPath()

    accounts = {

    }

    for smp in [i for i in os.listdir(smaPath) if not i.startswith('.')]:
        accounts[smp] = []
        for acc in [i for i in os.listdir(os.path.join(smaPath, smp)) if not i.startswith('.') and i.endswith('.sc')]:
            account = Account.from_path(smp, os.path.join(smaPath, smp, acc))

            account.load_settings(os.path.join(smaPath, smp))
            accounts[smp].append(account)
    
    return accounts

def deleteAccount(platform, username):
    try:
        sm_dir_path = f"{getSMAPath()}/{platform}"
        
        cookies_path = os.path.join(sm_dir_path, f"{username}.sc")
        if os.path.exists(cookies_path):
            os.remove(cookies_path)
            print(f"Deleted cookies for {platform}/{username}")
        
        settings_path = os.path.join(sm_dir_path, f"{username}_settings.json")
        if os.path.exists(settings_path):
            os.remove(settings_path)
            print(f"Deleted settings for {platform}/{username}")
        
        return True
    except Exception as e:
        print(f"Error deleting account {platform}/{username}: {e}")
        return False

def saveAccountSettings(account):
    try:
        sm_dir_path = f"{getSMAPath()}/{account.platform}"
        pathlib.Path(sm_dir_path).mkdir(parents=True, exist_ok=True)
        account.save_settings(sm_dir_path)
        return True
    except Exception as e:
        print(f"Error saving settings for {account.platform}/{account.username}: {e}")
        return False

def getAccountSettings(platform, username):
    try:
        sm_dir_path = f"{getSMAPath()}/{platform}"
        settings_path = os.path.join(sm_dir_path, f"{username}_settings.json")
        
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings_data = json.load(f)
                return AccountSettings.from_dict(settings_data)
        else:
            account_id = f"{platform}_{username}"
            return AccountSettings(account_id, platform, username)
    except Exception as e:
        print(f"Error loading settings for {platform}/{username}: {e}")
        account_id = f"{platform}_{username}"
        return AccountSettings(account_id, platform, username)

def updateAccountSettings(platform, username, **kwargs):
    try:
        settings = getAccountSettings(platform, username)
        
        for key, value in kwargs.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        
        sm_dir_path = f"{getSMAPath()}/{platform}"
        settings_path = os.path.join(sm_dir_path, f"{username}_settings.json")
        with open(settings_path, 'w') as f:
            json.dump(settings.to_dict(), f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error updating settings for {platform}/{username}: {e}")
        return False

def getEnabledAccounts():
    all_accounts = getAccounts()
    enabled_accounts = {}
    
    for platform, accounts in all_accounts.items():
        enabled_accounts[platform] = [acc for acc in accounts if acc.settings.enabled]
    
    return enabled_accounts

def categorize_post(post_text):
    if not client or not post_text or len(post_text) < 10:
        return "other"
    
    try:
        prompt = f"""
        Analyze the following social media post and categorize it into EXACTLY ONE of these categories:
        {', '.join(POST_CATEGORIES)}
        
        Post content:
        "{post_text}"
        
        Return ONLY the category name, nothing else.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=10,
        )
        
        category = response.choices[0].message.content.strip().lower()
        
        if category not in POST_CATEGORIES:
            return "other"
        
        return category
    
    except Exception as e:
        print(f"Error categorizing post: {e}")
        return "other"

def clean_post(post_data):
    if not client:
        return post_data['text']
    
    try:
        prompt = f"""
        Clean and format the following social media post to make it more readable as a news item.
        Remove unnecessary hashtags, emojis, and formatting while preserving the essential information.
        
        Original post:
        "{post_data['text']}"
        
        Return only the cleaned text.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            max_tokens=500,
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error cleaning post: {e}")
        return post_data['text']

def send_email(post_data, cleaned_content, account_settings=None):
    if account_settings and hasattr(post_data, 'category'):
        if post_data.get('category') not in account_settings.email_categories:
            return False
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_content = f"""
==========================================================
SENT: {timestamp}
FROM: news-aggregator@sniply.com
TO: user@example.com
SUBJECT: {post_data.get('category', 'General').title()} Update: Post from {post_data['username']}
----------------------------------------------------------
{cleaned_content}
----------------------------------------------------------
Original post by: {post_data['username']}
Post ID: {post_data['id']}
Category: {post_data.get('category', 'unknown')}
Platform: {post_data.get('platform', 'unknown')}
==========================================================

"""
        with open("sent_emails.txt", "a", encoding="utf-8") as f:
            f.write(email_content)
        
        return True
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return False