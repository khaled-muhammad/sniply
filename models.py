import json
import os
from pathlib import Path


class AccountSettings:
    def __init__(self, account_id, platform, username):
        self.account_id = account_id
        self.platform = platform
        self.username = username
        
        self.specific_pages = []
        self.email_categories = ["news"]
        self.enabled = True
        self.max_posts_per_scrape = 100
        self.scrape_interval_minutes = 30
        
        self.subreddits = []
        
        self.follow_users = []
        
    def to_dict(self):
        return {
            'account_id': self.account_id,
            'platform': self.platform,
            'username': self.username,
            'specific_pages': self.specific_pages,
            'email_categories': self.email_categories,
            'enabled': self.enabled,
            'max_posts_per_scrape': self.max_posts_per_scrape,
            'scrape_interval_minutes': self.scrape_interval_minutes,
            'subreddits': self.subreddits,
            'follow_users': self.follow_users
        }
    
    @classmethod
    def from_dict(cls, data):
        settings = cls(data['account_id'], data['platform'], data['username'])
        settings.specific_pages = data.get('specific_pages', [])
        settings.email_categories = data.get('email_categories', ["news"])
        settings.enabled = data.get('enabled', True)
        settings.max_posts_per_scrape = data.get('max_posts_per_scrape', 100)
        settings.scrape_interval_minutes = data.get('scrape_interval_minutes', 30)
        settings.subreddits = data.get('subreddits', [])
        settings.follow_users = data.get('follow_users', [])
        return settings


class Account:
    def __init__(self, platform, username, cookies, settings=None):
        self.platform = platform
        self.username = username
        self.cookies = cookies
        self.account_id = f"{platform}_{username}"
        self.settings = settings or AccountSettings(self.account_id, platform, username)
    
    @staticmethod
    def from_path(platform, path):
        with open(path, 'r') as f:
            cookies = json.load(f)
        
        username = path.split('/')[-1].removesuffix('.sc')
        account = Account(platform, username, cookies)
        
        settings_path = path.replace('.sc', '_settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings_data = json.load(f)
                account.settings = AccountSettings.from_dict(settings_data)
        
        return account
    
    def save_settings(self, base_path):
        settings_path = os.path.join(base_path, f"{self.username}_settings.json")
        with open(settings_path, 'w') as f:
            json.dump(self.settings.to_dict(), f, indent=2)
    
    def load_settings(self, base_path):
        settings_path = os.path.join(base_path, f"{self.username}_settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, 'r') as f:
                settings_data = json.load(f)
                self.settings = AccountSettings.from_dict(settings_data)
        else:
            self.settings = AccountSettings(self.account_id, self.platform, self.username)