import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from models import Account
from utils import categorize_post, clean_post, send_email

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")

service = Service(ChromeDriverManager().install())

def extract_post_id(post_url):
    """
    Extract a unique identifier for a Reddit post
    """
    try:
        if post_url:
            # Extract post ID from URL
            post_id = post_url.split('comments/')[1].split('/')[0]
            return post_id
    except Exception as e:
        pass
    
    # Fallback: Generate a timestamp-based ID
    import time
    return f"post_{int(time.time() * 1000)}"

def startRedditScraping(account: Account):
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://reddit.com/")
    sleep(3)

    print("Authenticating ...")

    for cookie in account.cookies:
        cookie.pop("sameSite", None)
        driver.add_cookie(cookie)

    driver.refresh()
    print("Logged in using cookies!")

    # Try to close overlay if present
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[data-testid="secondary-button"][title="Continue"] svg[icon-name="close-outline"]'
            ))
        )
        actual_button = button.find_element(By.XPATH, "./ancestor::button[1]")
        actual_button.click()
        print("Closed overlay!")
    except TimeoutException:
        print("Specific close-outline button not found within 10 seconds.")

    # Set to store unique post IDs to prevent duplicates
    seen_posts = set()
    unique_posts = []
    
    # Counter for news posts sent to email
    news_posts_count = 0
    
    # Scroll and process posts with smart scrolling
    last_height = driver.execute_script("return document.body.scrollHeight")
    posts_found_in_last_scroll = 0
    consecutive_empty_scrolls = 0
    max_consecutive_empty_scrolls = 3
    scroll_count = 0
    
    while scroll_count < 10000:  # Maximum scroll limit
        try:
            feed = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "shreddit-feed"))
            )
            
            print(f"Processing feed on scroll {scroll_count+1}")
            
            posts = feed.find_elements(By.TAG_NAME, 'shreddit-post')
            
            print(f"Found: {len(posts)} posts on scroll {scroll_count+1}")
            
            # Track new posts found in this scroll
            new_posts_this_scroll = 0

            for post in posts:
                try:
                    post_url = post.find_element(By.CSS_SELECTOR, 'a[slot="full-post-link"]').get_attribute("href")
                    post_id = extract_post_id(post_url)
                    
                    # Skip if we've seen this post before
                    if post_id in seen_posts:
                        continue
                    
                    # Mark this post as seen and increment new posts counter
                    seen_posts.add(post_id)
                    new_posts_this_scroll += 1
                    
                    # Extract post text
                    post_text = None
                    try:
                        element = post.find_element(By.CSS_SELECTOR, 'faceplate-screen-reader-content')
                        post_text = element.text
                    except:
                        pass
                    
                    # Extract subreddit name
                    subreddit = None
                    try:
                        subreddit_element = post.find_element(By.CSS_SELECTOR, 'a[data-click-id="subreddit"]')
                        subreddit = subreddit_element.text
                    except:
                        pass
                    
                    # Extract username
                    username = None
                    try:
                        username_element = post.find_element(By.CSS_SELECTOR, 'a[data-click-id="user"]')
                        username = username_element.text
                    except:
                        pass
                    
                    # Extract media URLs
                    media_urls = []

                    # 1. Single image post
                    try:
                        single_imgs = post.find_elements(By.CSS_SELECTOR, "shreddit-aspect-ratio img.media-lightbox-img")
                        for img in single_imgs:
                            src = img.get_attribute("src")
                            if src:
                                media_urls.append(src)
                    except:
                        pass

                    # 2. Carousel images
                    try:
                        carousel_imgs = post.find_elements(By.CSS_SELECTOR, "gallery-carousel li figure img")
                        for img in carousel_imgs:
                            src = img.get_attribute("src")
                            if src:
                                media_urls.append(src)
                    except:
                        pass

                    # 3. Videos
                    try:
                        video_players = post.find_elements(By.CSS_SELECTOR, "shreddit-player-2")
                        for player in video_players:
                            # First try the <source> tag
                            try:
                                source = player.find_element(By.TAG_NAME, "source")
                                src = source.get_attribute("src")
                                if src:
                                    media_urls.append(src)
                                    continue
                            except:
                                pass
                            # Fallback to video.src attribute
                            video_src = player.get_attribute("src")
                            if video_src:
                                media_urls.append(video_src)
                    except:
                        pass

                    # Store post data
                    post_data = {
                        'id': post_id,
                        'username': username or "Unknown User",
                        'subreddit': subreddit or "Unknown Subreddit",
                        'text': post_text or "",
                        'url': post_url,
                        'media': media_urls
                    }
                    
                    # Skip posts with no meaningful content
                    if not post_text or len(post_text) < 10:
                        print(f"Post {post_id} has no meaningful text. Skipping...")
                        continue
                    
                    # Categorize the post
                    category = categorize_post(post_text)
                    post_data['category'] = category
                    
                    # If it's a news post, clean it and send to email
                    if category == "news":
                        cleaned_content = clean_post(post_data)
                        if send_email(post_data, cleaned_content):
                            news_posts_count += 1
                            print(f"News post from r/{post_data['subreddit']} sent to email")
                    
                    # Add to unique posts
                    unique_posts.append(post_data)
                    
                    # Output
                    print(f"Post ID: {post_id}")
                    print(f"Subreddit: {post_data['subreddit']}")
                    print(f"Username: {post_data['username']}")
                    print(f"Category: {category}")
                    print(f"Post URL: {post_url}")
                    print(f"Post Text: {post_text[:100]}..." if post_text and len(post_text) > 100 else f"Post Text: {post_text}")
                    print(f"Media: {media_urls}")
                    print("=====================")
                    
                except Exception as e:
                    print(f"Error processing post: {e}")
                    continue
            
            # Update tracking variables
            posts_found_in_last_scroll = new_posts_this_scroll
            
            # Smart scrolling logic
            if new_posts_this_scroll == 0:
                consecutive_empty_scrolls += 1
                print(f"No new posts found. Consecutive empty scrolls: {consecutive_empty_scrolls}")
            else:
                consecutive_empty_scrolls = 0
                print(f"Found {new_posts_this_scroll} new posts this scroll")
            
            # If we've had too many consecutive empty scrolls, try different scrolling strategies
            if consecutive_empty_scrolls >= max_consecutive_empty_scrolls:
                print("Trying aggressive scrolling due to consecutive empty scrolls...")
                # Try scrolling to absolute bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(5)
                
                # Reset counter after aggressive scroll
                consecutive_empty_scrolls = 0
            else:
                # Adaptive smooth scrolling based on content found
                current_position = driver.execute_script("return window.pageYOffset;")
                scroll_height = driver.execute_script("return document.body.scrollHeight")
                viewport_height = driver.execute_script("return window.innerHeight")
                
                # Adjust scroll speed based on content discovery
                if new_posts_this_scroll > 5:
                    # Lots of content, scroll slower to process more
                    scroll_step = viewport_height // 4
                    scroll_iterations = 3
                    sleep_between = 1.5
                elif new_posts_this_scroll > 0:
                    # Some content, normal scrolling
                    scroll_step = viewport_height // 3
                    scroll_iterations = 4
                    sleep_between = 1
                else:
                    # No content, scroll faster
                    scroll_step = viewport_height // 2
                    scroll_iterations = 6
                    sleep_between = 0.5
                
                # Perform adaptive smooth scrolling
                for i in range(scroll_iterations):
                    driver.execute_script(f"window.scrollBy(0, {scroll_step});")
                    sleep(sleep_between)
                    
                    # Check if we've reached the bottom during scrolling
                    current_pos = driver.execute_script("return window.pageYOffset;")
                    total_height = driver.execute_script("return document.body.scrollHeight")
                    if current_pos + viewport_height >= total_height - 100:  # Near bottom
                        print("Reached near bottom during smooth scroll")
                        break
                
                sleep(2)  # Additional wait for content to load
            
            # Check if page height changed (new content loaded)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height and consecutive_empty_scrolls >= max_consecutive_empty_scrolls:
                print("No new content loaded and multiple empty scrolls. Stopping.")
                break
            
            last_height = new_height
            scroll_count += 1
            
        except TimeoutException:
            print("shreddit-feed did not appear within 5 seconds.")
            break
    
    # Summary
    print(f"\nScraping Summary:")
    print(f"Total unique posts processed: {len(unique_posts)}")
    print(f"News posts sent to email: {news_posts_count}")
    
    # Keep the browser window open
    input("Press Enter to close the browser...")
    driver.quit()