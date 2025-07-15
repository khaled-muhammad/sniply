import random
from utils import saveAuth, POST_CATEGORIES
from demo_mode import DEMO_USERS, DEMO_SUBREDDITS

def add_demo_account():
    print("Let’s add a demo account")
    print("Which platform?")
    print("1) Facebook")
    print("2) Twitter (X)")
    print("3) LinkedIn")
    print("4) Reddit")
    print("5) Back")
    
    while True:
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            platform = "facebook"
            users = [u for u in DEMO_USERS[platform] if not u.startswith('demo_')]
            break
        elif choice == "2":
            platform = "x"
            users = [u for u in DEMO_USERS[platform] if not u.startswith('demo_')]
            break
        elif choice == "3":
            platform = "linkedin"
            users = [u for u in DEMO_USERS[platform] if not u.startswith('demo_')]
            break
        elif choice == "4":
            platform = "reddit"
            users = [u for u in DEMO_USERS[platform] if not u.startswith('demo_')]
            break
        elif choice == "5":
            return
        else:
            print("Invalid choice. Try again.")
            continue
    
    print(f"\nCreating a fake {platform.title()} account...")
    print("(No real login needed)")
    
    print("\nPick a username:")
    print("1) Random from list")
    print("2) Type your own")
    
    user_choice = input("Enter choice: ").strip()
    
    if user_choice == "1":
        username = random.choice(users)
    elif user_choice == "2":
        name = input("Your username: ").strip()
        username = name or f"demo_{random.randint(1000,9999)}"
    else:
        username = random.choice(users)
    
    print(f"Done: demo account {platform}/{username}")
    
    # Create mock cookies
    mock_cookies = [
        {'name': 'session_id', 'value': f'demo_session_{username}_{random.randint(1000, 9999)}'},
        {'name': 'auth_token', 'value': f'demo_token_{username}'},
        {'name': 'user_id', 'value': str(random.randint(100000, 999999))},
        {'name': 'csrf_token', 'value': f'csrf_{random.randint(10000, 99999)}'}
    ]
    
    try:
        saveAuth(platform, username, mock_cookies)
        print("Account saved. You can tweak its settings next.")
        if input("Edit its settings now? (y/n)").lower() == 'y':
            configure_demo_account_settings(platform, username)
    except Exception as err:
        print(f"Oops, couldn’t save account: {err}")

def configure_demo_account_settings(platform, username):
    print(f"\nSettings for {platform}/{username}")
    
    print(f"\nCategories: {', '.join(POST_CATEGORIES)}")
    categories_input = input("Enter categories (comma-separated) or press Enter for default: ").strip()
    
    if categories_input:
        categories = [cat.strip().lower() for cat in categories_input.split(',') if cat.strip() in POST_CATEGORIES]
    else:
        categories = ["news"]
    
    # Max posts
    max_posts_input = input("Max posts per scrape (default 100): ").strip()
    try:
        max_posts = int(max_posts_input) if max_posts_input else 100
    except ValueError:
        max_posts = 100
    
    # Interval
    interval_input = input("Scrape interval in minutes (default 30): ").strip()
    try:
        interval = int(interval_input) if interval_input else 30
    except ValueError:
        interval = 30
    
    # Extra platform settings
    subreddits = []
    follow_users = []
    
    if platform == 'reddit':
        subs_input = input(f"Subreddits to follow (default: {', '.join(DEMO_SUBREDDITS[:3])}): ").strip()
        if subs_input:
            subreddits = [sub.strip() for sub in subs_input.split(',') if sub.strip()]
        else:
            subreddits = DEMO_SUBREDDITS[:3]
    
    elif platform in ['facebook', 'x', 'linkedin']:
        users_input = input("Users/pages to follow (comma-separated): ").strip()
        if users_input:
            follow_users = [user.strip() for user in users_input.split(',') if user.strip()]
    
    from utils import updateAccountSettings
    
    success = updateAccountSettings(
        platform, username,
        email_categories=categories,
        max_posts_per_scrape=max_posts,
        scrape_interval_minutes=interval,
        subreddits=subreddits,
        follow_users=follow_users
    )
    
    print("Settings updated." if success else "Failed to update settings.")

if __name__ == '__main__':
    add_demo_account()