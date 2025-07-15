import json
import os
import random
from datetime import datetime, timedelta
from models import Account
from utils import POST_CATEGORIES, getSMAPath, categorize_post, clean_post, send_email
import pathlib

DEMO_POSTS = {
    'news': [
        "Breaking: New climate change report shows unprecedented warming trends across the globe. Scientists warn of critical tipping points approaching faster than expected.",
        "Economic markets rally as inflation shows signs of cooling. Federal Reserve considers policy adjustments in upcoming meeting.",
        "Local election results: Progressive candidate wins by narrow margin, promising housing reforms and environmental initiatives.",
        "Tech company announces major layoffs affecting thousands of employees worldwide. Stock prices drop 15% in after-hours trading.",
        "Healthcare breakthrough: New treatment shows promising results for previously incurable disease affecting millions globally."
    ],
    'technology': [
        "AI model achieves human-level performance in complex reasoning tasks. Researchers publish findings in leading science journal.",
        "New smartphone features revolutionary battery technology lasting 5 days on single charge. Pre-orders begin next month.",
        "Quantum computing milestone reached as system solves problem impossible for classical computers in minutes.",
        "Social media platform introduces end-to-end encryption for all messages. Privacy advocates celebrate the decision.",
        "Electric vehicle sales surge 200% year-over-year as charging infrastructure expands rapidly across major cities."
    ],
    'sports': [
        "Championship game ends in dramatic overtime victory. Record-breaking attendance of 75,000 fans witness historic match.",
        "Star athlete announces retirement after 15-year career. Hall of Fame induction ceremony planned for next year.",
        "Underdog team defeats favorites in stunning upset. Coach credits improved training methods and team chemistry.",
        "Olympic preparations underway as athletes gear up for upcoming games. New records expected in multiple events.",
        "Trade deadline shakeup: Three major players switch teams in blockbuster deal worth $200 million."
    ],
    'entertainment': [
        "Blockbuster movie breaks opening weekend records with $150 million domestic box office. Sequel already in development.",
        "Award-winning series gets renewed for three more seasons. Streaming platform invests heavily in original content.",
        "Music festival lineup announced featuring top artists from around the world. Tickets sell out in record time.",
        "Celebrity couple announces engagement after two years of dating. Wedding planned for next summer in private ceremony.",
        "Documentary about environmental crisis wins prestigious film award. Director dedicates victory to climate activists."
    ],
    'lifestyle': [
        "New study reveals benefits of Mediterranean diet for brain health. Researchers recommend specific foods for cognitive function.",
        "Minimalist living trend grows as people seek simpler lifestyles. Experts share tips for decluttering and mindful consumption.",
        "Urban gardening movement spreads to apartment dwellers. Vertical farming solutions make fresh produce accessible to city residents.",
        "Wellness retreat bookings surge as people prioritize mental health. Meditation and yoga programs see unprecedented demand.",
        "Sustainable fashion brands gain popularity among conscious consumers. Fast fashion industry faces growing criticism."
    ],
    'personal': [
        "Finally finished my marathon training! 26.2 miles here I come. Thanks to everyone who supported me on this journey.",
        "Celebrating 5 years at my dream job today. Grateful for amazing colleagues and opportunities to grow professionally.",
        "Just adopted the sweetest rescue dog. She's already stolen my heart and made our house feel like a real home.",
        "Moved to a new city and loving the adventure. Exploring local coffee shops and making new friends every day.",
        "Graduated from night school after 3 years of hard work. Proof that it's never too late to pursue your dreams."
    ],
    'meme': [
        "When you realize it's Monday again... *internal screaming intensifies* Why does the weekend go by so fast?",
        "Me: I'll go to bed early tonight. Also me at 2 AM: Just one more episode... or five more episodes.",
        "That moment when you're an adult but still ask your mom for advice on literally everything. Some things never change.",
        "Trying to eat healthy: *buys vegetables* Same vegetables a week later: *have become science experiments in the fridge*",
        "When someone asks if you're ready for the meeting you forgot about: *nervous laughter* Define 'ready'..."
    ],
    'advertisement': [
        "Limited time offer: Get 50% off premium subscription! Upgrade now and unlock exclusive features. Use code SAVE50 at checkout.",
        "New product launch: Revolutionary fitness tracker with 30-day battery life. Pre-order now and get free shipping worldwide.",
        "Flash sale: Designer clothing up to 70% off. Hurry, limited stock available. Shop now before it's gone forever.",
        "Introducing our latest software update with AI-powered features. Download today and experience the future of productivity.",
        "Special promotion: Buy two, get one free on all skincare products. Transform your routine with our award-winning formulas."
    ]
}

DEMO_USERS = {
    'facebook': ['john_doe', 'sarah_smith', 'mike_johnson', 'lisa_brown', 'demo_user'],
    'x': ['techguru2024', 'newshound', 'sportswriter', 'foodie_life', 'demo_tweeter'],
    'reddit': ['reddit_user_123', 'news_reader', 'tech_enthusiast', 'casual_browser', 'demo_redditor'],
    'linkedin': ['professional_user', 'industry_expert', 'career_coach', 'startup_founder', 'demo_linkedin']
}

DEMO_SUBREDDITS = ['technology', 'news', 'worldnews', 'sports', 'entertainment', 'lifestyle', 'funny', 'memes']

def create_demo_accounts():
    # build demo accounts
    demo_accounts = {}
    
    for platform in ['facebook', 'x', 'reddit', 'linkedin']:
        demo_accounts[platform] = []
        
        for username in DEMO_USERS[platform]:
            # Create mock cookies
            mock_cookies = [
                {'name': 'session_id', 'value': f'demo_session_{username}_{random.randint(1000, 9999)}'},
                {'name': 'auth_token', 'value': f'demo_token_{username}'},
                {'name': 'user_id', 'value': str(random.randint(100000, 999999))}
            ]
            
            # Create account with demo settings
            account = Account(platform, username, mock_cookies)
            
            account.settings.enabled = random.choice([True, True, True, False])
            account.settings.max_posts_per_scrape = random.choice([50, 100, 150, 200])
            account.settings.scrape_interval_minutes = random.choice([15, 30, 45, 60])
            account.settings.email_categories = random.sample(POST_CATEGORIES, random.randint(2, 5))
            
            if platform == 'reddit':
                account.settings.subreddits = random.sample(DEMO_SUBREDDITS, random.randint(2, 4))
            elif platform in ['facebook', 'x', 'linkedin']:
                account.settings.follow_users = [f'user_{i}' for i in range(random.randint(1, 5))]
            
            demo_accounts[platform].append(account)
    
    return demo_accounts

def generate_demo_posts(account, num_posts=None):
    # build fake posts
    if num_posts is None:
        num_posts = min(account.settings.max_posts_per_scrape, random.randint(20, 50))
    
    posts = []
    categories = list(DEMO_POSTS.keys())
    
    for i in range(num_posts):
        category = random.choice(categories)
        post_text = random.choice(DEMO_POSTS[category])
        
        if random.random() < 0.3:
            extra_content = [
                " What do you think about this?",
                " Share your thoughts in the comments!",
                " This is really important to consider.",
                " I found this fascinating.",
                " Worth sharing with everyone."
            ]
            post_text += random.choice(extra_content)
        
        username = random.choice(DEMO_USERS[account.platform])
        
        post_data = {
            'id': f'demo_post_{account.platform}_{i}_{random.randint(1000, 9999)}',
            'username': username,
            'text': post_text,
            'category': category,
            'platform': account.platform,
            'timestamp': datetime.now() - timedelta(hours=random.randint(0, 72))
        }
        
        # Add platform-specific data
        if account.platform == 'reddit':
            post_data['subreddit'] = random.choice(DEMO_SUBREDDITS)
            post_data['url'] = f'https://reddit.com/r/{post_data["subreddit"]}/comments/{post_data["id"]}'
        elif account.platform == 'x':
            post_data['images'] = []
            if random.random() < 0.2:  # 20% chance of having images
                post_data['images'] = [f'https://demo.com/image_{random.randint(1, 100)}.jpg']
        elif account.platform == 'linkedin':
            post_data['profile_url'] = f'https://linkedin.com/in/{username}'
        
        posts.append(post_data)
    
    return posts

def save_demo_accounts(demo_accounts):
    # write demo accounts to disk
    for platform, accounts in demo_accounts.items():
        platform_dir = os.path.join(getSMAPath(), platform)
        pathlib.Path(platform_dir).mkdir(parents=True, exist_ok=True)
        
        for account in accounts:
            # Save cookies
            cookies_path = os.path.join(platform_dir, f"{account.username}.sc")
            with open(cookies_path, 'w') as f:
                json.dump(account.cookies, f)
            
            # Save settings
            account.save_settings(platform_dir)

def simulate_scraping(account):
    print(f"Running demo scrape: {account.platform}/{account.username}")
    print(f"Email categories: {', '.join(account.settings.email_categories)}")
    print(f"Max posts per scrape: {account.settings.max_posts_per_scrape}")
    
    if account.settings.specific_pages:
        print(f"Specific pages: {len(account.settings.specific_pages)} configured")
    
    if account.platform == 'reddit' and account.settings.subreddits:
        print(f"Subreddits: {', '.join(account.settings.subreddits)}")
    
    posts = generate_demo_posts(account)
    
    emailed = 0
    for post in posts:
        # Check if this category should be emailed
        if post['category'] in account.settings.email_categories:
            cleaned_content = clean_post(post)
            if send_email(post, cleaned_content, account.settings):
                emailed += 1
        
        print("-- post info --")
        print(f"Post ID: {post['id']}")
        print(f"Username: {post['username']}")
        print(f"Category: {post['category']}")
        if account.platform == 'reddit':
            print(f"Subreddit: {post['subreddit']}")
        print(f"Text: {post['text'][:100]}...")
        print("=" * 50)
    
    print("Demo scrape done.")
    print(f"Processed {len(posts)} posts, emailed {emailed} items.")
    
    return posts

def setup_demo_mode():
    print("Turning on demo mode...")
    
    # Create demo accounts
    demo_accounts = create_demo_accounts()
    
    # Save them to file system
    save_demo_accounts(demo_accounts)
    
    count = sum(len(accs) for accs in demo_accounts.values())
    print(f"Demo mode ready, {count} accounts created.")
    
    return demo_accounts

def cleanup_demo_mode():
    try:
        sma_path = getSMAPath()
        
        for platform in ['facebook', 'x', 'reddit', 'linkedin']:
            platform_dir = os.path.join(sma_path, platform)
            if os.path.exists(platform_dir):
                for file in os.listdir(platform_dir):
                    if file.startswith('demo_') or any(demo_user in file for demo_user in DEMO_USERS[platform]):
                        file_path = os.path.join(platform_dir, file)
                        os.remove(file_path)
        
        # Clear demo emails
        if os.path.exists('sent_emails.txt'):
            open('sent_emails.txt', 'w').close()
        
        print("Demo mode off, data cleared.")
        return True
    except Exception as e:
        print(f"Error cleaning up demo mode: {e}")
        return False

def is_demo_mode():
    try:
        sma_path = getSMAPath()
        for platform in ['facebook', 'x', 'reddit', 'linkedin']:
            platform_dir = os.path.join(sma_path, platform)
            if os.path.exists(platform_dir):
                for file in os.listdir(platform_dir):
                    if any(demo_user in file for demo_user in DEMO_USERS[platform]):
                        return True
        return False
    except:
        return False

if __name__ == '__main__':
    opt = input("Demo mode (1 on, 2 off, 3 status): ")
    if opt == '1':
        setup_demo_mode()
    elif opt == '2':
        cleanup_demo_mode()
    elif opt == '3':
        print("Active" if is_demo_mode() else "Inactive")
    else:
        print("No action taken.")