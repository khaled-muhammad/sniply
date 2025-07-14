from models import Account
from scrappers.facebook_scrapper import startFacebookScraping
from scrappers.linkedIn_scrapper import startLinkedInScraping
from scrappers.reddit_scrapper import startRedditScraping
from scrappers.x_scrapper import startXScraping
from utils import getEnabledAccounts
from colorama import Fore, Style


def start():
    print(f"\n{Fore.CYAN}=== Starting Sniply Scraping ==={Style.RESET_ALL}")
    
    # Get only enabled accounts
    accs = getEnabledAccounts()
    
    if not accs:
        print(f"{Fore.YELLOW}No enabled accounts found. Please add and enable accounts first.{Style.RESET_ALL}")
        return
    
    total_accounts = sum(len(accounts) for accounts in accs.values())
    print(f"Found {total_accounts} enabled account(s) to process...")
    
    for provider, accounts in accs.items():
        for account in accounts:
            print(f"\n{Fore.GREEN}Starting scraping for {provider.capitalize()}/{account.username}{Style.RESET_ALL}")
            print(f"Email categories: {', '.join(account.settings.email_categories)}")
            print(f"Max posts per scrape: {account.settings.max_posts_per_scrape}")
            
            if account.settings.specific_pages:
                print(f"Specific pages: {len(account.settings.specific_pages)} configured")
            
            if provider == 'facebook':
                startFacebookScraping(account=account)
            elif provider == 'x':
                startXScraping(account=account)
            elif provider == 'reddit':
                startRedditScraping(account=account)
            elif provider == 'linkedin':
                startLinkedInScraping(account=account)
            else:
                print(f"{Fore.YELLOW}Unknown platform: {provider}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}=== Scraping completed for all enabled accounts ==={Style.RESET_ALL}")