from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
import re
import json

def extract_username(html_content):
    pattern1 = r'<span[^>]*class="[^"]*f2 a[^"]*"[^>]*role="link"[^>]*>([^<]+)</span>'
    
    pattern2 = r'aria-label="([^"]+) Profile Picture'
    
    matches = re.findall(pattern1, html_content)
    if matches:
        return matches[0].strip()
    
    matches = re.findall(pattern2, html_content)
    if matches:
        return matches[0].strip()
    
    return None

def extract_post_id(html_content):
    """
    Extract unique post identifiers from Facebook post HTML content.
    Returns a dictionary with multiple possible IDs to ensure uniqueness.
    """
    post_ids = {}
    
    # Method 1: Extract data-tracking-duration-id (most reliable for feed posts)
    pattern_tracking_id = r'data-tracking-duration-id="([^"]+)"'
    tracking_id_match = re.search(pattern_tracking_id, html_content)
    if tracking_id_match:
        post_ids['tracking_id'] = tracking_id_match.group(1)
    
    # Method 2: Extract video_id for video posts
    pattern_video_id = r'data-video-id="([^"]+)"'
    video_id_match = re.search(pattern_video_id, html_content)
    if video_id_match:
        post_ids['video_id'] = video_id_match.group(1)
    
    # Method 3: Extract top_level_post_id from tracking data
    pattern_tracking_data = r'data-video-tracking=\'([^\']+)\''
    tracking_data_match = re.search(pattern_tracking_data, html_content)
    if tracking_data_match:
        try:
            tracking_json = json.loads(tracking_data_match.group(1))
            if 'top_level_post_id' in tracking_json:
                post_ids['top_level_post_id'] = tracking_json['top_level_post_id']
            if 'content_owner_id_new' in tracking_json:
                post_ids['content_owner_id'] = tracking_json['content_owner_id_new']
        except:
            pass
    
    # Method 4: For image posts, extract image_id
    pattern_image_id = r'data-image-id="([^"]+)"'
    image_id_matches = re.findall(pattern_image_id, html_content)
    if image_id_matches and len(image_id_matches) > 0:
        post_ids['image_id'] = image_id_matches[0]  # Use the first image ID
    
    # Method 5: Fallback - create a hash from username + timestamp + first few words of content
    username = extract_username(html_content)
    if username:
        post_ids['username'] = username
        
        # Try to extract timestamp
        timestamp_pattern = r'<span[^>]*style="[^"]*color: #8a8d91[^"]*"[^>]*class="f5"[^>]*>([^<]+)</span>'
        timestamp_match = re.search(timestamp_pattern, html_content)
        if timestamp_match:
            post_ids['timestamp'] = timestamp_match.group(1).strip()
    
    return post_ids