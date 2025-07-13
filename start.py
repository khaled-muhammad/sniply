from models import Account
from scrappers.facebook_scrapper import startFacebookScraping
from scrappers.reddit_scrapper import startRedditScraping
from scrappers.x_scrapper import startXScraping
from utils import getAccounts


def start():
    accs = getAccounts()

    for provider, accounts in accs.items():
        # if provider == 'facebook':
        #     for account in accounts:
        #         print(f"Starting Listening on Account: {account['account_name']}")
        #         startFacebookScraping(account=Account.from_path(provider, account['path']))
        # if provider == 'x':
        #     for account in accounts:
        #         print(f"Starting Listening on Account: {account['account_name']}")
        #         startXScraping(account=Account.from_path(provider, account['path']))
        if provider == 'reddit':
            for account in accounts:
                print(f"Starting Listening on Account: {account['account_name']}")
                startRedditScraping(account=Account.from_path(provider, account['path']))