from utils import getAccounts, updateAccountSettings, getAccountSettings, POST_CATEGORIES
from models import AccountSettings

def run_settings_demo():
    print("="*60)
    print("Sniply Settings Demo")
    print("="*60, "\n")

    print("Key Features:")
    print("- Per-account email categories and post limits.")
    print("- Scrape specific pages, subreddits, or user profiles.")
    print("- Toggle accounts on/off without deleting.")
    print("- Settings are saved automatically.")
    print("\nTo configure, run the main app and choose option 3.\n")
    print("-" * 60)

    accounts = getAccounts()
    if not accounts:
        print("No accounts found. Please add an account first.")
        return

    print("Current Account Status:")
    for platform, accs in accounts.items():
        print(f"\n{platform.capitalize()}:")
        for account in accs:
            status = "enabled" if account.settings.enabled else "disabled"
            print(f"  - {account.username} ({status})")

    print("\n" + "="*60)
    print("Demonstrating Settings Updates...")
    print("="*60 + "\n")

    demo_account = None
    demo_platform = ""
    for platform, accs in accounts.items():
        if accs:
            demo_account = accs[0]
            demo_platform = platform
            break

    if not demo_account:
        print("No accounts available for demo.")
        return

    print(f"Using account: {demo_platform}/{demo_account.username}\n")

    print("Updating email categories...")
    new_categories = ["news", "technology", "sports"]
    if updateAccountSettings(demo_platform, demo_account.username, email_categories=new_categories):
        print(f"   New categories set: {', '.join(new_categories)}")

    print("\nSetting max posts limit...")
    if updateAccountSettings(demo_platform, demo_account.username, max_posts_per_scrape=50):
        print("   Limit set to 50.")

    if demo_platform == 'reddit':
        print("\nAdding subreddits...")
        specific_subreddits = ["technology", "news", "programming"]
        if updateAccountSettings(demo_platform, demo_account.username, subreddits=specific_subreddits):
            print(f"   Now tracking subreddits: {', '.join(specific_subreddits)}")

    print("\nAdding specific pages for scraping...")
    specific_pages = ["https://example.com/news", "https://example.com/tech"]
    if updateAccountSettings(demo_platform, demo_account.username, specific_pages=specific_pages):
        print(f"   Now scraping {len(specific_pages)} specific pages.")

    print("\n" + "="*60)
    print(f"Final settings for {demo_account.username}:")
    updated_settings = getAccountSettings(demo_platform, demo_account.username)
    if updated_settings:
        print(f"   Email categories: {', '.join(updated_settings.email_categories)}")
        print(f"   Max posts: {updated_settings.max_posts_per_scrape}")
        if updated_settings.specific_pages:
            print(f"   Specific pages: {len(updated_settings.specific_pages)}")
        if demo_platform == 'reddit' and updated_settings.subreddits:
            print(f"   Subreddits: {', '.join(updated_settings.subreddits)}")
    print("="*60)

    print("\nAvailable Post Categories:")
    for i, category in enumerate(POST_CATEGORIES, 1):
        print(f" {i}. {category}")

    print("\nDemo finished. Settings were updated for the test account.")
    print("You can manage all accounts from the main menu (option 3).")


if __name__ == '__main__':
    run_settings_demo() 