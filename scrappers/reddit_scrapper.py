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
    try:
        if post_url:
            post_id = post_url.split('comments/')[1].split('/')[0]
            return post_id
    except Exception as e:
        pass
    
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

    seen_posts = set()
    unique_posts = []
    news_posts_count = 0
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    posts_found_in_last_scroll = 0
    consecutive_empty_scrolls = 0
    max_consecutive_empty_scrolls = 8
    scroll_count = 0
    last_post_count = 0
    stagnant_cycles = 0
    loading_indicators_checked = 0
    total_aggressive_attempts = 0
    scroll_positions = []
    
    while scroll_count < 10000:
        try:
            feed = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "shreddit-feed"))
            )
            
            loading_indicators = driver.find_elements(By.CSS_SELECTOR, 
                "shreddit-loading, [data-testid='loading'], .loading, shreddit-async-loader")
            
            if loading_indicators:
                print(f"Loading indicators detected: {len(loading_indicators)} (ignoring for now)")
                loading_indicators_checked += 1
                sleep(1)
            
            print(f"Processing feed on scroll {scroll_count+1}")
            
            posts = feed.find_elements(By.TAG_NAME, 'shreddit-post')
            current_post_count = len(posts)
            
            print(f"Found: {current_post_count} total posts on scroll {scroll_count+1}")
            
            if current_post_count == last_post_count:
                stagnant_cycles += 1
                print(f"Post count stagnant for {stagnant_cycles} cycles (will try {15 - stagnant_cycles} more times)")
            else:
                stagnant_cycles = 0
            
            last_post_count = current_post_count
            new_posts_this_scroll = 0

            for post in posts:
                try:
                    post_url = post.find_element(By.CSS_SELECTOR, 'a[slot="full-post-link"]').get_attribute("href")
                    post_id = extract_post_id(post_url)
                    
                    if post_id in seen_posts:
                        continue
                    
                    seen_posts.add(post_id)
                    new_posts_this_scroll += 1
                    
                    post_text = None
                    try:
                        element = post.find_element(By.CSS_SELECTOR, 'faceplate-screen-reader-content')
                        post_text = element.text
                    except:
                        pass
                    
                    subreddit = None
                    try:
                        subreddit_element = post.find_element(By.CSS_SELECTOR, 'a[data-click-id="subreddit"]')
                        subreddit = subreddit_element.text
                    except:
                        pass
                    
                    username = None
                    try:
                        username_element = post.find_element(By.CSS_SELECTOR, 'a[data-click-id="user"]')
                        username = username_element.text
                    except:
                        pass
                    
                    media_urls = []

                    try:
                        single_imgs = post.find_elements(By.CSS_SELECTOR, "shreddit-aspect-ratio img.media-lightbox-img")
                        for img in single_imgs:
                            src = img.get_attribute("src")
                            if src:
                                media_urls.append(src)
                    except:
                        pass

                    try:
                        carousel_imgs = post.find_elements(By.CSS_SELECTOR, "gallery-carousel li figure img")
                        for img in carousel_imgs:
                            src = img.get_attribute("src")
                            if src:
                                media_urls.append(src)
                    except:
                        pass

                    try:
                        video_players = post.find_elements(By.CSS_SELECTOR, "shreddit-player-2")
                        for player in video_players:
                            try:
                                source = player.find_element(By.TAG_NAME, "source")
                                src = source.get_attribute("src")
                                if src:
                                    media_urls.append(src)
                                    continue
                            except:
                                pass
                            video_src = player.get_attribute("src")
                            if video_src:
                                media_urls.append(video_src)
                    except:
                        pass

                    post_data = {
                        'id': post_id,
                        'username': username or "Unknown User",
                        'subreddit': subreddit or "Unknown Subreddit",
                        'text': post_text or "",
                        'url': post_url,
                        'media': media_urls
                    }
                    
                    if not post_text or len(post_text) < 10:
                        print(f"Post {post_id} has no meaningful text. Skipping...")
                        continue
                    
                    category = categorize_post(post_text)
                    post_data['category'] = category
                    
                    if category == "news":
                        cleaned_content = clean_post(post_data)
                        if send_email(post_data, cleaned_content):
                            news_posts_count += 1
                            print(f"News post from r/{post_data['subreddit']} sent to email")
                    
                    unique_posts.append(post_data)
                    
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
            
            posts_found_in_last_scroll = new_posts_this_scroll
            current_position = driver.execute_script("return window.pageYOffset;")
            scroll_positions.append(current_position)
            
            if len(scroll_positions) > 5:
                scroll_positions.pop(0)
            
            position_stuck = len(scroll_positions) >= 5 and all(
                abs(pos - scroll_positions[0]) < 20 for pos in scroll_positions
            )
            
            if new_posts_this_scroll == 0:
                consecutive_empty_scrolls += 1
                print(f"No new posts found. Consecutive empty scrolls: {consecutive_empty_scrolls}")
            else:
                consecutive_empty_scrolls = 0
                print(f"Found {new_posts_this_scroll} new posts this scroll")
            
            viewport_height = driver.execute_script("return window.innerHeight")
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            
            if position_stuck or stagnant_cycles >= 15:
                print("AGGRESSIVE MODE: Position stuck or too many stagnant cycles")
                total_aggressive_attempts += 1
                
                techniques = [
                    "window.scrollTo(0, document.body.scrollHeight);",
                    f"window.scrollBy(0, {viewport_height * 5});",
                    "window.scrollTo(0, document.body.scrollHeight - 2000);",
                    f"window.scrollBy(0, {viewport_height * 8});",
                    "window.scrollTo(0, document.body.scrollHeight - 500);",
                    f"window.scrollBy(0, {viewport_height * 10});"
                ]
                
                for i, technique in enumerate(techniques):
                    print(f"Trying aggressive technique {i+1}/{len(techniques)}")
                    driver.execute_script(technique)
                    sleep(3)
                    
                    new_posts_check = len(driver.find_elements(By.TAG_NAME, 'shreddit-post'))
                    if new_posts_check > current_post_count:
                        print(f"Technique {i+1} worked! Found {new_posts_check - current_post_count} new posts")
                        break
                    
                    for j in range(3):
                        driver.execute_script(f"window.scrollBy(0, {viewport_height});")
                        sleep(1)
                    
                sleep(6)
                stagnant_cycles = 0
                
            elif loading_indicators and loading_indicators_checked < 50:
                print("LOADING MODE: Detected loading indicators (being aggressive)")
                
                for _ in range(5):
                    driver.execute_script(f"window.scrollBy(0, {viewport_height // 2});")
                    sleep(1)
                
                sleep(2)
                
            elif consecutive_empty_scrolls >= max_consecutive_empty_scrolls:
                print("SEARCH MODE: Multiple empty scrolls, searching for content")
                
                scroll_distances = [viewport_height // 2, viewport_height, viewport_height * 1.5]
                
                for distance in scroll_distances:
                    driver.execute_script(f"window.scrollBy(0, {distance});")
                    sleep(1.5)
                    
                    quick_posts = len(driver.find_elements(By.TAG_NAME, 'shreddit-post'))
                    if quick_posts > current_post_count:
                        print(f"Found content with {distance}px scroll")
                        break
                
                consecutive_empty_scrolls = 0
                
            else:
                print("ADAPTIVE MODE: Normal content-aware scrolling")
                
                if new_posts_this_scroll > 8:
                    scroll_step = viewport_height // 6
                    scroll_iterations = 2
                    sleep_between = 2
                elif new_posts_this_scroll > 3:
                    scroll_step = viewport_height // 4
                    scroll_iterations = 3
                    sleep_between = 1.5
                elif new_posts_this_scroll > 0:
                    scroll_step = viewport_height // 3
                    scroll_iterations = 4
                    sleep_between = 1
                else:
                    scroll_step = viewport_height // 2
                    scroll_iterations = 5
                    sleep_between = 0.8
                
                for i in range(scroll_iterations):
                    driver.execute_script(f"window.scrollBy(0, {scroll_step});")
                    sleep(sleep_between)
                    
                    if i == scroll_iterations // 2:
                        mid_posts = len(driver.find_elements(By.TAG_NAME, 'shreddit-post'))
                        if mid_posts > current_post_count:
                            print(f"Content loaded mid-scroll: {mid_posts - current_post_count} new posts")
                    
                    current_pos = driver.execute_script("return window.pageYOffset;")
                    total_height = driver.execute_script("return document.body.scrollHeight")
                    if current_pos + viewport_height >= total_height - 100:
                        print("Reached near bottom during adaptive scroll")
                        break
                
                sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            
            should_stop = (
                (new_height == last_height and 
                 consecutive_empty_scrolls >= max_consecutive_empty_scrolls and 
                 stagnant_cycles >= 20 and 
                 total_aggressive_attempts >= 5) or
                (position_stuck and stagnant_cycles >= 25 and total_aggressive_attempts >= 3) or
                (scroll_count > 500)
            )
            
            if should_stop:
                print(f"Really stopping now: scroll_count={scroll_count}, stagnant_cycles={stagnant_cycles}, aggressive_attempts={total_aggressive_attempts}")
                break
            
            last_height = new_height
            scroll_count += 1
            
        except TimeoutException:
            print("shreddit-feed did not appear within 5 seconds.")
            break
    
    print(f"\nScraping Summary:")
    print(f"Total unique posts processed: {len(unique_posts)}")
    print(f"News posts sent to email: {news_posts_count}")
    
    input("Press Enter to close the browser...")
    driver.quit()