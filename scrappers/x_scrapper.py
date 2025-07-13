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
from selenium_helpers import extract_username
from utils import categorize_post, clean_post, send_email

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")

service = Service(ChromeDriverManager().install())

def extract_tweet_id(tweet_element):
    """
    Extract a unique identifier for a tweet
    """
    try:
        # Try to get the tweet link which contains the tweet ID
        links = tweet_element.find_elements(By.XPATH, './/a[contains(@href, "/status/")]')
        for link in links:
            href = link.get_attribute('href')
            if href and '/status/' in href:
                # Extract the tweet ID from the URL
                tweet_id = href.split('/status/')[1].split('?')[0].split('/')[0]
                return tweet_id
    except Exception as e:
        pass
    
    # Fallback: Generate a composite ID from username and tweet text
    try:
        username_links = tweet_element.find_elements(By.XPATH, './/a[starts-with(@href, "/")]')
        username = None
        for link in username_links:
            if link.text.strip():
                username = link.text.strip()
                break
                
        if username:
            # Get a snippet of the tweet text for uniqueness
            try:
                tweet_text_element = tweet_element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                tweet_snippet = tweet_text_element.text[:20].strip()
                return f"user_{username}_{tweet_snippet}"
            except:
                pass
    except:
        pass
    
    # Last resort: Use a timestamp
    import time
    return f"tweet_{int(time.time() * 1000)}"

def startXScraping(account: Account):
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load X (Twitter)
    driver.get("https://x.com/")
    sleep(3)

    print("Authenticating ...")

    for cookie in account.cookies:
        # Handle domain issues
        cookie.pop("sameSite", None)  # Avoid errors in some versions
        driver.add_cookie(cookie)

    # Reload page with cookies set
    driver.refresh()
    print("Logged in using cookies!")
    sleep(5)
    
    # Set to store unique tweet IDs to prevent duplicates
    seen_tweets = set()
    unique_tweets = []
    
    # Dictionary to track tweets with no text content across scrolls
    pending_tweets = {}
    
    # Counter for news tweets sent to email
    news_tweets_count = 0
    
    # Scroll and process tweets
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for scroll_count in range(1000):
        # Find all tweet articles
        tweets = driver.find_elements(By.TAG_NAME, 'article')
        print(f"Found {len(tweets)} tweets on scroll {scroll_count+1}")
        
        # Process pending tweets from previous scroll first
        pending_ids_to_remove = []
        
        for tweet_id, tweet_data in pending_tweets.items():
            # Check if the tweet now has content
            if 'element_id' in tweet_data:
                try:
                    # Try to find the tweet element again
                    updated_tweet = driver.find_element(By.ID, tweet_data['element_id'])
                    
                    # Try to get updated text
                    try:
                        tweet_text_element = updated_tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                        updated_text = tweet_text_element.text.strip()
                        
                        # Check if the tweet now has content
                        if updated_text and len(updated_text) > 10:  # Arbitrary threshold for meaningful content
                            tweet_data['text'] = updated_text
                            
                            # Categorize the tweet
                            category = categorize_post(updated_text)
                            tweet_data['category'] = category
                            
                            # If it's a news tweet, clean it and send to email
                            if category == "news":
                                cleaned_content = clean_post(tweet_data)
                                if send_email(tweet_data, cleaned_content):
                                    news_tweets_count += 1
                                    print(f"News tweet from {tweet_data['username']} sent to email")
                            
                            unique_tweets.append(tweet_data)
                            pending_ids_to_remove.append(tweet_id)
                            
                            print(f"Added previously pending tweet ID: {tweet_id}")
                            print("Username:", tweet_data['username'])
                            print("Category:", category)
                            print("==============")
                            print(updated_text)
                            print("\n")
                    except:
                        # Still can't get text, keep it pending
                        pass
                except:
                    # Tweet might not be visible anymore, keep it pending for one more scroll
                    pass
        
        # Remove processed pending tweets
        for tweet_id in pending_ids_to_remove:
            del pending_tweets[tweet_id]
        
        # Process newly found tweets
        for tweet in tweets:
            try:
                # Extract tweet ID
                tweet_id = extract_tweet_id(tweet)
                
                # Skip if we've seen this tweet before or it's pending
                if not tweet_id or tweet_id in seen_tweets or tweet_id in pending_tweets:
                    continue
                
                # Extract username
                username_links = tweet.find_elements(By.XPATH, './/a[starts-with(@href, "/")]')
                username = None
                for link in username_links:
                    if link.text.strip():
                        username = link.text.strip()
                        break
                
                if not username:
                    print("No valid username found in tweet.")
                    continue
                
                # Extract tweet text
                tweet_text = ""
                try:
                    tweet_text_element = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    tweet_text = tweet_text_element.text.strip()
                except:
                    pass
                
                # Extract images
                image_elements = tweet.find_elements(By.TAG_NAME, "img")
                image_srcs = [img.get_attribute("src") for img in image_elements if img.get_attribute("src")]
                
                # Get tweet element ID if possible (for finding it again later)
                element_id = tweet.get_attribute("id") or ""
                
                # Store tweet data
                tweet_data = {
                    'id': tweet_id,
                    'username': username,
                    'text': tweet_text,
                    'images': image_srcs,
                    'element_id': element_id
                }
                
                # Check if tweet has meaningful text content
                if not tweet_text or len(tweet_text) < 10:  # Arbitrary threshold for meaningful content
                    # Add to pending tweets to check on next scroll
                    pending_tweets[tweet_id] = tweet_data
                    print(f"Tweet {tweet_id} has no meaningful text. Adding to pending...")
                    continue
                
                # Mark this tweet as seen
                seen_tweets.add(tweet_id)
                
                # Categorize the tweet
                category = categorize_post(tweet_text)
                tweet_data['category'] = category
                
                # If it's a news tweet, clean it and send to email
                if category == "news":
                    cleaned_content = clean_post(tweet_data)
                    if send_email(tweet_data, cleaned_content):
                        news_tweets_count += 1
                        print(f"News tweet from {username} sent to email")
                
                # Add to unique tweets
                unique_tweets.append(tweet_data)
                
                # Output
                print(f"Tweet ID: {tweet_id}")
                print("Username:", username)
                print("Category:", category)
                print("Tweet   :", tweet_text)
                print("Images  :", image_srcs)
                print("=====================")
            
            except Exception as e:
                print("Skipped a tweet due to error:", e)
        
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(5)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached bottom or no new content loaded.")
            break
        last_height = new_height
        
        # If this is the last scroll, add any remaining pending tweets that still have some text
        if scroll_count == 999:
            for tweet_id, tweet_data in pending_tweets.items():
                if tweet_data.get('text'):  # If it has any text at all
                    # Categorize the tweet
                    category = categorize_post(tweet_data['text'])
                    tweet_data['category'] = category
                    
                    # If it's a news tweet, clean it and send to email
                    if category == "news":
                        cleaned_content = clean_post(tweet_data)
                        if send_email(tweet_data, cleaned_content):
                            news_tweets_count += 1
                            print(f"News tweet from {tweet_data['username']} sent to email")
                    
                    seen_tweets.add(tweet_id)
                    unique_tweets.append(tweet_data)
                    print(f"Adding pending tweet on final scroll: {tweet_id}")
    
    print(f"Total unique tweets found: {len(unique_tweets)}")
    print(f"Tweets skipped due to no content: {len(pending_tweets)}")
    print(f"News tweets sent to email: {news_tweets_count}")
    return unique_tweets