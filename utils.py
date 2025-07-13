import json
import os
import pathlib
from groq import Groq
from datetime import datetime

# Initialize Groq client
try:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
except Exception as e:
    print(f"Warning: Could not initialize Groq client: {e}")
    client = None

# Predefined categories for posts
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
    p = f"{os.path.expanduser("~/sniply")}/sm_accs/"
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
        for acc in [i for i in os.listdir(os.path.join(smaPath, smp)) if not i.startswith('.')]:
            accounts[smp].append({'account_name': acc.removesuffix('.sc'), 'path': os.path.join(smaPath, smp, acc)})
    
    return accounts

def categorize_post(post_text):
    """
    Categorize a post using Groq LLM
    """
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
            max_tokens=10,  # We only need a single word response
        )
        
        category = response.choices[0].message.content.strip().lower()
        
        # Ensure the category is valid
        if category not in POST_CATEGORIES:
            return "other"
        
        return category
    
    except Exception as e:
        print(f"Error categorizing post: {e}")
        return "other"

def clean_post(post_data):
    """
    Clean a post using Groq LLM to make it more readable
    """
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

def send_email(post_data, cleaned_content):
    """
    Simulate sending an email by appending to sent_emails.txt
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        email_content = f"""
==========================================================
SENT: {timestamp}
FROM: news-aggregator@sniply.com
TO: user@example.com
SUBJECT: News Update: Post from {post_data['username']}
----------------------------------------------------------
{cleaned_content}
----------------------------------------------------------
Original post by: {post_data['username']}
Post ID: {post_data['id']}
==========================================================

"""
        with open("sent_emails.txt", "a", encoding="utf-8") as f:
            f.write(email_content)
        
        return True
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return False