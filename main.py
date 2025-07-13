import sys

from add_account import add_account
from start import start
from view_accounts import viewAccounts


print("Welcome to Sniply, Only the posts worth your time")
print("Please choose an option:")
print("1- Start")
print("2- View connected Social Media")
print("3- Add new account")
choice = input("Enter your choice: ")

if choice == '1':
    start()
elif choice == '2':
    viewAccounts()
elif choice == '3':
    add_account()
else:
    print("Bye, see you soon!")
    sys.exit()