import os
import glob
from selenium_helpers import extract_username, extract_post_id

def test_post_id_extraction():
    """
    Test the post ID extraction functionality on the saved HTML files
    """
    print("Testing post ID extraction from HTML files...")
    
    # Create a set to track unique IDs
    seen_ids = set()
    
    # Process all HTML files in the posts_html directory
    for html_file in sorted(glob.glob('posts_html/post_*.html')):
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        # Extract post IDs
        post_ids = extract_post_id(html_content)
        
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
        
        # Extract username
        username = extract_username(html_content)
        
        print(f"File: {html_file}")
        print(f"Username: {username}")
        print(f"Unique ID: {post_unique_id}")
        print(f"All IDs: {post_ids}")
        
        # Check if this ID was seen before
        if post_unique_id in seen_ids:
            print("DUPLICATE POST DETECTED!")
        else:
            seen_ids.add(post_unique_id)
            
        print("-" * 50)

if __name__ == "__main__":
    test_post_id_extraction()