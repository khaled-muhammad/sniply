from demo_mode import simulate_scraping, is_demo_mode
from models import Account
from utils import getEnabledAccounts

def facebook_demo_scrape(account: Account):
    return simulate_scraping(account)

def x_demo_scrape(account: Account):
    return simulate_scraping(account)

def reddit_demo_scrape(account: Account):
    return simulate_scraping(account)

def linkedin_demo_scrape(account: Account):
    return simulate_scraping(account)

def run_demo_scrape():
    if not is_demo_mode():
        print("Demo mode isn’t on. Run it first.")
        return
    print("Running demo scraping...")
    accounts = getEnabledAccounts()
    if not accounts:
        print("Nothing to do.")
        return
    count = sum(len(accs) for accs in accounts.values())
    print(f"We have {count} demo accounts here.")
    all_posts = []
    for platform, accs in accounts.items():
        for acct in accs:
            print(f"Now on {platform}/{acct.username}")
            if platform == 'facebook':
                posts = facebook_demo_scrape(acct)
            elif platform == 'x':
                posts = x_demo_scrape(acct)
            elif platform == 'reddit':
                posts = reddit_demo_scrape(acct)
            elif platform == 'linkedin':
                posts = linkedin_demo_scrape(acct)
            else:
                print(f"Skip unknown: {platform}")
                continue
            all_posts += posts
    print("All done with demo scraping.")
    print(f"Total posts: {len(all_posts)}")
    return all_posts

if __name__ == '__main__':
    run_demo_scrape()