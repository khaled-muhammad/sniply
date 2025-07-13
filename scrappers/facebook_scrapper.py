import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from models import Account
from selenium_helpers import extract_username, extract_post_id
from utils import categorize_post, clean_post, send_email

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")

service = Service(ChromeDriverManager().install())


def startFacebookScraping(account: Account):
    driver  = webdriver.Chrome(service=service, options=chrome_options)

    # Load Facebook
    driver.get("https://www.facebook.com/")
    sleep(3)

    print("Authenticating ...")

    for cookie in account.cookies:
        # Handle domain issues
        cookie.pop("sameSite", None)  # Avoid errors in some vers
        driver.add_cookie(cookie)

    # Reload page with cookies set
    driver.get("https://m.facebook.com/")
    print("Logged in using cookies!")
    sleep(5)
    posts_container = driver.find_element(By.XPATH, "//div[@data-pull-to-refresh-size]")
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # Set to store unique post IDs to prevent duplicates
    seen_posts = set()
    unique_posts = []
    
    # Dictionary to track posts with no text content across scrolls
    pending_posts = {}
    
    # Counter for news posts sent to email
    news_posts_count = 0

    for scroll_count in range(1000):
        posts = posts_container.find_elements(By.XPATH, "//div[@data-tracking-duration-id]")
        
        # Process pending posts from previous scroll first
        pending_ids_to_remove = []
        
        for post_id, post_data in pending_posts.items():
            # Try to find the post again in the current view
            try:
                updated_post = driver.find_element(By.XPATH, f"//div[@data-tracking-duration-id='{post_data['tracking_id']}']")
                updated_text = updated_post.text.strip()
                
                # Check if the post now has content
                if updated_text and len(updated_text) > 10:  # Arbitrary threshold for meaningful content
                    post_data['text'] = updated_text
                    
                    # Categorize the post
                    category = categorize_post(updated_text)
                    post_data['category'] = category
                    
                    # If it's a news post, clean it and send to email
                    if category == "news":
                        cleaned_content = clean_post(post_data)
                        if send_email(post_data, cleaned_content):
                            news_posts_count += 1
                            print(f"News post from {post_data['username']} sent to email")
                    
                    unique_posts.append(post_data)
                    pending_ids_to_remove.append(post_id)
                    
                    print(f"Added previously pending post ID: {post_id}")
                    print("Username:", post_data['username'])
                    print("Category:", category)
                    print("==============")
                    print(updated_text)
                    print("\n")
            except:
                # Post might not be visible anymore, keep it pending for one more scroll
                pass
        
        # Remove processed pending posts
        for post_id in pending_ids_to_remove:
            del pending_posts[post_id]
            
        # Process newly found posts
        for i, post in enumerate(posts, start=1):
            try:
                html = post.get_attribute("outerHTML")
            except:
                continue
            
            # Extract post IDs to check for duplicates
            post_ids = extract_post_id(html)
            
            # Create a unique identifier from the post_ids
            post_unique_id = None
            
            # Try to use the most reliable IDs in order of preference
            if 'top_level_post_id' in post_ids:
                post_unique_id = f"top_level_{post_ids['top_level_post_id']}"
            elif 'tracking_id' in post_ids:
                post_unique_id = f"tracking_{post_ids['tracking_id']}"
            elif 'video_id' in post_ids:
                post_unique_id = f"video_{post_ids['video_id']}"
            elif 'image_id' in post_ids:
                post_unique_id = f"image_{post_ids['image_id']}"
            elif 'username' in post_ids and 'timestamp' in post_ids:
                # Create a composite ID if no better option exists
                post_unique_id = f"user_{post_ids['username']}_{post_ids['timestamp']}"
            
            # Skip if we've seen this post before, couldn't generate an ID, or it's pending
            if not post_unique_id or post_unique_id in seen_posts or post_unique_id in pending_posts:
                continue
                
            # Extract username
            username = extract_username(html)
            if username is None:
                continue
            
            # Get post text content
            post_text = post.text.strip()
            
            # Store post data
            post_data = {
                'id': post_unique_id,
                'username': username,
                'text': post_text,
                'html': html,
                'ids': post_ids,
                'tracking_id': post_ids.get('tracking_id', '')
            }
            
            # Check if post has meaningful text content
            if not post_text or len(post_text) < 10:  # Arbitrary threshold for meaningful content
                # Add to pending posts to check on next scroll
                pending_posts[post_unique_id] = post_data
                print(f"Post {post_unique_id} has no meaningful text. Adding to pending...")
                continue
            
            # Mark this post as seen
            seen_posts.add(post_unique_id)
            
            # Categorize the post
            category = categorize_post(post_text)
            post_data['category'] = category
            
            # If it's a news post, clean it and send to email
            if category == "news":
                cleaned_content = clean_post(post_data)
                if send_email(post_data, cleaned_content):
                    news_posts_count += 1
                    print(f"News post from {username} sent to email")
            
            # Add to unique posts
            unique_posts.append(post_data)
            
            print(f"Post ID: {post_unique_id}")
            print("Username:", username)
            print("Category:", category)
            print("==============")
            print(post_text)
            print("\n")
        
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("Reached bottom or no new content loaded.")
            break
        last_height = new_height
        
        # If this is the last scroll, add any remaining pending posts that still have no text
        if scroll_count == 9:
            for post_id, post_data in pending_posts.items():
                if post_data['text']:  # If it has any text at all
                    # Categorize the post
                    category = categorize_post(post_data['text'])
                    post_data['category'] = category
                    
                    # If it's a news post, clean it and send to email
                    if category == "news":
                        cleaned_content = clean_post(post_data)
                        if send_email(post_data, cleaned_content):
                            news_posts_count += 1
                            print(f"News post from {post_data['username']} sent to email")
                    
                    seen_posts.add(post_id)
                    unique_posts.append(post_data)
                    print(f"Adding pending post on final scroll: {post_id}")
    
    print(f"Total unique posts found: {len(unique_posts)}")
    print(f"Posts skipped due to no content: {len(pending_posts)}")
    print(f"News posts sent to email: {news_posts_count}")
    return unique_posts