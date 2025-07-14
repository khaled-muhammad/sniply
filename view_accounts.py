import os
from colorama import Fore, Style

from utils import getAccounts, getSMAPath

smaPath = getSMAPath()

def viewAccounts():
    accs = getAccounts()
    
    if not accs:
        print(f"{Fore.YELLOW}No accounts found.{Style.RESET_ALL}")
        print("Use option 4 in the main menu to add accounts.")
        return

    print(f"\n{Fore.CYAN}=== Connected Social Media Accounts ==={Style.RESET_ALL}")
    
    total_accounts = 0
    enabled_accounts = 0
    
    for provider, accounts in accs.items():
        print(f"\n{Fore.GREEN}{provider.capitalize()}:{Style.RESET_ALL}")
        
        if not accounts:
            print(f"  {Fore.YELLOW}No accounts configured{Style.RESET_ALL}")
            continue
            
        for account in accounts:
            total_accounts += 1
            status_color = Fore.GREEN if account.settings.enabled else Fore.RED
            status_text = "✓ Enabled" if account.settings.enabled else "✗ Disabled"
            
            if account.settings.enabled:
                enabled_accounts += 1
            
            print(f"  • {Fore.CYAN}{account.username}{Style.RESET_ALL} - {status_color}{status_text}{Style.RESET_ALL}")
            
            # Show email categories
            if account.settings.email_categories:
                categories_text = ", ".join(account.settings.email_categories)
                print(f"    Email categories: {categories_text}")
            else:
                print(f"    {Fore.YELLOW}No email categories configured{Style.RESET_ALL}")
            
            # Show specific pages/configurations
            if account.settings.specific_pages:
                print(f"    Specific pages: {len(account.settings.specific_pages)} configured")
            
            # Platform-specific settings
            if provider == 'reddit' and account.settings.subreddits:
                subreddits_text = ", ".join(f"r/{sub}" for sub in account.settings.subreddits)
                print(f"    Subreddits: {subreddits_text}")
            
            if provider in ['facebook', 'x', 'linkedin'] and account.settings.follow_users:
                users_text = ", ".join(account.settings.follow_users)
                print(f"    Following: {users_text}")
            
            print(f"    Max posts per scrape: {account.settings.max_posts_per_scrape}")
    
    print(f"\n{Fore.CYAN}Summary:{Style.RESET_ALL}")
    print(f"Total accounts: {total_accounts}")
    print(f"Enabled accounts: {Fore.GREEN}{enabled_accounts}{Style.RESET_ALL}")
    print(f"Disabled accounts: {Fore.RED}{total_accounts - enabled_accounts}{Style.RESET_ALL}")
    
    if enabled_accounts == 0:
        print(f"\n{Fore.YELLOW}No accounts are enabled for scraping.{Style.RESET_ALL}")
        print("Use option 3 in the main menu to manage account settings.")

if __name__ == '__main__':
    viewAccounts()