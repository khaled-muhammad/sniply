import os
import glob
import json
from selenium_helpers import extract_username, extract_post_id
from utils import categorize_post, clean_post, send_email

def test_post_categorization():
    """
    Test post categorization, cleaning, and email functionality on the saved HTML files
    """
    print("Testing post categorization and email functionality...")
    
    # Create a set to track unique IDs
    seen_posts = set()
    categorized_posts = {}
    news_posts_count = 0
    
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
        
        # Skip if we've seen this post before or couldn't generate an ID
        if not post_unique_id or post_unique_id in seen_posts:
            continue
            
        seen_posts.add(post_unique_id)
        
        # Extract username and text content
        username = extract_username(html_content)
        
        # Extract text content from the HTML (simple approach)
        import re
        text_content = ""
        text_divs = re.findall(r'<div[^>]*class="native-text[^>]*>(.*?)</div>', html_content, re.DOTALL)
        for div in text_divs:
            # Extract text from spans
            spans = re.findall(r'<span[^>]*>(.*?)</span>', div, re.DOTALL)
            for span in spans:
                if len(span) > 5 and not span.startswith('See more'):
                    text_content += span + " "
        
        text_content = text_content.strip()
        
        # Skip if no meaningful text content
        if not text_content or len(text_content) < 10:
            continue
        
        # Create post data structure
        post_data = {
            'id': post_unique_id,
            'username': username if username else "Unknown User",
            'text': text_content,
            'file': html_file
        }
        
        # Categorize the post
        print(f"Categorizing post from {html_file}...")
        category = categorize_post(text_content)
        post_data['category'] = category
        
        # Add to categorized posts
        if category not in categorized_posts:
            categorized_posts[category] = []
        categorized_posts[category].append(post_data)
        
        print(f"File: {html_file}")
        print(f"Username: {username}")
        print(f"Category: {category}")
        print("Preview:", text_content[:100] + "..." if len(text_content) > 100 else text_content)
        
        # If it's a news post, clean it and send to email
        if category == "news":
            print("Processing news post...")
            cleaned_content = clean_post(post_data)
            if send_email(post_data, cleaned_content):
                news_posts_count += 1
                print(f"News post from {username} sent to email")
                
        print("-" * 50)
    
    # Print summary
    print("\nCategorization Summary:")
    for category, posts in categorized_posts.items():
        print(f"{category}: {len(posts)} posts")
    
    print(f"\nTotal news posts sent to email: {news_posts_count}")
    
    # Check if sent_emails.txt was created
    if os.path.exists("sent_emails.txt"):
        print("\nEmails were successfully sent to sent_emails.txt")
    else:
        print("\nNo emails were sent")

if __name__ == "__main__":
    # Check if GROQ_API_KEY is set
    if not os.environ.get("GROQ_API_KEY"):
        print("Warning: GROQ_API_KEY environment variable is not set.")
        print("Using fallback categorization method.")
        
        # Set a temporary environment variable for testing
        # In a real scenario, you would set this in your environment
        os.environ["GROQ_API_KEY"] = "YOUR_API_KEY_HERE"
        print("Set a placeholder API key for demonstration purposes.")
        print("In a real scenario, please set your actual Groq API key.")
    
    test_post_categorization() 