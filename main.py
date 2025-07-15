import sys
from colorama import Fore

from add_account import add_account
from start import start
from view_accounts import viewAccounts
from manage_accounts import run_account_manager
from demo_mode import setup_demo_mode, cleanup_demo_mode, is_demo_mode
from demo_scraper import start_demo_scraping
from demo_add_account import demo_add_account

print(Fore.GREEN + """
 ░▒▓███████▓▒░▒▓███████▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░    ░▒▓██████▓▒░  
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░     
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░     
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░     
                                                                      
""" + Fore.RESET)

print("Welcome to Sniply, Only the posts worth your time")

# Check if we're in demo mode
demo_active = is_demo_mode()
if demo_active:
    print(f"{Fore.YELLOW}🎮 DEMO MODE ACTIVE{Fore.RESET}")

print("\nPlease choose an option:")
print("1- Start Scraping")
print("2- View Connected Accounts")
print("3- Manage Accounts (Settings, Delete, Re-auth)")
print("4- Add New Account")
print("5- Demo Mode")
print("6- Exit")

choice = input("Enter your choice: ")

if choice == '1':
    if demo_active:
        print("Starting demo scraping...")
        start_demo_scraping()
    else:
        start()
elif choice == '2':
    viewAccounts()
elif choice == '3':
    run_account_manager()
elif choice == '4':
    if demo_active:
        demo_add_account()
    else:
        add_account()
elif choice == '5':
    print("\nDemo Mode Options:")
    print("1- Setup Demo Mode (creates test accounts)")
    print("2- Cleanup Demo Mode (removes test accounts)")
    print("3- Demo Status")
    print("4- Back to main menu")
    
    demo_choice = input("Enter demo choice: ")
    
    if demo_choice == '1':
        if demo_active:
            print("Demo mode already active. Cleanup first to reset.")
        else:
            setup_demo_mode()
            print("Demo mode setup complete! You can now test all features.")
    elif demo_choice == '2':
        if cleanup_demo_mode():
            print("Demo mode cleaned up successfully!")
        else:
            print("Error cleaning up demo mode.")
    elif demo_choice == '3':
        status = "Active" if demo_active else "Inactive"
        print(f"Demo mode status: {status}")
    elif demo_choice == '4':
        print("Returning to main menu...")
    else:
        print("Invalid demo choice.")
elif choice == '6':
    print("Bye, see you soon!")
    sys.exit()
else:
    print("Invalid choice. Please run the program again.")
    sys.exit()