import os
import sys
from colorama import Fore, Style
from utils import getAccounts as fetch_accounts, deleteAccount as delete_account, saveAccountSettings as store_settings, POST_CATEGORIES as CATEGORIES
from add_account import add_account as add_new_account

def show_summary(acct):
    print(f"\n> {acct.platform.capitalize()}/{acct.username}")
    status = 'On' if acct.settings.enabled else 'Off'
    color = Fore.GREEN if acct.settings.enabled else Fore.RED
    print(f"  Status: {color}{status}{Style.RESET_ALL}")
    print(f"  Max posts: {acct.settings.max_posts_per_scrape}")
    print(f"  Interval: every {acct.settings.scrape_interval_minutes}m")
    if acct.settings.email_categories:
        print("  Emails: " + ", ".join(acct.settings.email_categories))
    if acct.settings.specific_pages:
        print("  Pages: " + ", ".join(acct.settings.specific_pages))
    if acct.platform == 'reddit' and acct.settings.subreddits:
        print("  Subs: " + ", ".join(acct.settings.subreddits))
    if acct.platform in ['facebook', 'x', 'linkedin'] and acct.settings.follow_users:
        print("  Follows: " + ", ".join(acct.settings.follow_users))

def tweak_settings(acct):
    while True:
        print(f"\nSettings for {acct.username}@{acct.platform}")
        opts = [
            "Toggle on/off",
            "Email categories",
            "Pages/URLs",
            "Max posts",
            "Interval"
        ]
        for i, o in enumerate(opts, 1):
            print(f"{i}) {o}")
        if acct.platform == 'reddit':
            print("6) Subreddits")
        else:
            print("6) Follow list")
        print("7) Save & Return")
        print("8) Cancel\n")
        choice = input("Pick> ").strip()
        if choice == '1':
            acct.settings.enabled = not acct.settings.enabled
            print("Enabled" if acct.settings.enabled else "Disabled")
        elif choice == '2':
            print("Available:", ", ".join(CATEGORIES))
            cats = input("New cats> ").strip().lower()
            if cats == 'all':
                acct.settings.email_categories = CATEGORIES.copy()
            else:
                picks = [c.strip() for c in cats.split(',') if c.strip() in CATEGORIES]
                acct.settings.email_categories = picks
                if len(picks) != len([c.strip() for c in cats.split(',')]):
                    print("Some were ignored")
            print("Now:", ", ".join(acct.settings.email_categories))
        elif choice == '3':
            pages = acct.settings.specific_pages
            print("Pages:", ", ".join(pages) if pages else "None yet")
            action = input("Add(a), Remove(r), Clear(c), Back(b)> ").strip().lower()
            if action == 'a':
                url = input("URL> ").strip()
                if url and url not in pages:
                    pages.append(url)
                    print("Added")
            elif action == 'r':
                idx = input("Index> ").strip()
                if idx.isdigit() and 1 <= int(idx) <= len(pages):
                    rem = pages.pop(int(idx)-1)
                    print(f"Removed {rem}")
            elif action == 'c':
                pages.clear()
                print("Cleared")
        elif choice == '4':
            val = input(f"Max posts ({acct.settings.max_posts_per_scrape})> ").strip()
            if val.isdigit() and int(val) > 0:
                acct.settings.max_posts_per_scrape = int(val)
                print("Set")
        elif choice == '5':
            val = input(f"Interval ({acct.settings.scrape_interval_minutes})> ").strip()
            if val.isdigit() and int(val) > 0:
                acct.settings.scrape_interval_minutes = int(val)
                print("Set")
        elif choice == '6':
            if acct.platform == 'reddit':
                subs = input("Subs> ").strip()
                acct.settings.subreddits = [s.strip() for s in subs.split(',') if s.strip()]
                print("Subs now:", ", ".join(acct.settings.subreddits))
            else:
                follows = input("Follows> ").strip()
                acct.settings.follow_users = [u.strip() for u in follows.split(',') if u.strip()]
                print("Follows now:", ", ".join(acct.settings.follow_users))
        elif choice == '7':
            ok = store_settings(acct)
            print("Saved!" if ok else "Save failed")
            return
        elif choice == '8':
            print("Canceled")
            return
        else:
            print("Try again")

def handle_account(provider, acct_list):
    if not acct_list:
        print(f"No {provider} accounts at all")
        return
    print(f"\n{provider.capitalize()} Accounts:")
    for idx, acct in enumerate(acct_list, 1):
        mark = Fore.GREEN+'✓'+Style.RESET_ALL if acct.settings.enabled else Fore.RED+'✗'+Style.RESET_ALL
        print(f"{idx}) {acct.username} {mark}")
    sel = input("Pick> ").strip()
    if not sel.isdigit() or not (1 <= int(sel) <= len(acct_list)):
        print("Bad choice")
        return
    acct = acct_list[int(sel)-1]
    while True:
        show_summary(acct)
        print("\nActions:")
        print("1) Edit settings")
        print("2) Re-authenticate")
        print("3) Delete")
        print("4) Back")
        cmd = input("Choose> ").strip()
        if cmd == '1':
            tweak_settings(acct)
        elif cmd == '2':
            confirm = input("Re-login? y/n> ").strip().lower()
            if confirm == 'y':
                delete_account(provider, acct.username)
                print("Log in again")
                add_new_account()
                return
        elif cmd == '3':
            confirm = input("Type DELETE to remove> ").strip()
            if confirm == 'DELETE':
                ok = delete_account(provider, acct.username)
                print("Deleted" if ok else "Delete failed")
                return
            else:
                print("Cancel")
        elif cmd == '4':
            return
        else:
            print("Try again")

def run_account_manager():
    while True:
        all_accts = fetch_accounts()
        print("\nYour Accounts:")
        if not all_accts:
            print("None yet")
            print("1) Add new")
            print("2) Back")
            opt = input("Pick> ").strip()
            if opt == '1':
                add_new_account()
            else:
                return
            continue
        providers = list(all_accts.keys())
        for idx, prov in enumerate(providers, 1):
            acs = all_accts[prov]
            on = sum(1 for a in acs if a.settings.enabled)
            tot = len(acs)
            print(f"{idx}) {prov.capitalize()}: {on}/{tot} on")
        print(f"{len(providers)+1}) Add new")
        print(f"{len(providers)+2}) Back")
        opt = input("Pick> ").strip()
        if opt.isdigit():
            num = int(opt)
            if 1 <= num <= len(providers):
                handle_account(providers[num-1], all_accts[providers[num-1]])
            elif num == len(providers)+1:
                add_new_account()
            elif num == len(providers)+2:
                return
            else:
                print("Try again")
        else:
            print("Numbers only")

if __name__ == '__main__':
    run_account_manager()