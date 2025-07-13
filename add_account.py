import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import saveAuth

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())

#FB, X, LinkedIn, Reddit
def add_account():
    print("Please, choose a social media platform to use: ")
    print("1- Facebook")
    print("2- Twitter (X)")
    print("3- LinkedIn")
    print("4- Reddit")
    print("5- To go back")

    while True:
        choice = input("Enter a choice: ")

        if choice == "1":
            print("You selected to add a new Facebook account.")
            print("Please, login in the pop up ............")
            try:
                driver  = webdriver.Chrome(service=service, options=chrome_options)
                driver.get("https://www.facebook.com/")
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'form[action^="/logout.php"]')
                    )
                )
                print("Logged In Successfully!")
                driver.get("https://www.facebook.com/me")
                WebDriverWait(driver, 10).until(EC.url_changes("https://www.facebook.com/me"))
                profile_url = driver.current_url
                username    = profile_url.split("/")[-2]

                print("Your username:", username)

                time.sleep(10)

                cookies = driver.get_cookies()

                saveAuth(
                    platform_name='facebook',
                    username=username,
                    cookies=cookies
                )
            except:
                print("Time limit, exceeded! Please try again.")
        elif choice == "2":
            #https://x.com/
            print("You selected to add a new X account.")
            print("Please, login in the pop up ............")
            try:
                driver  = webdriver.Chrome(service=service, options=chrome_options)
                driver.get("https://x.com/")
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'button[aria-label^="Account menu"]')
                    )
                )
                print("Logged In Successfully!")
                username_link_tag = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-testid="AppTabBar_Profile_Link"]')))
                username = username_link_tag.get_attribute("href").split('/')[-1]
                print("Your username:", username)

                time.sleep(10)

                cookies = driver.get_cookies()

                saveAuth(
                    platform_name='x',
                    username=username,
                    cookies=cookies
                )
            except:
                print("Time limit, exceeded! Please try again.")
        elif choice == "3":
            pass
        elif choice == "4":
            print("You selected to add a new Reddit account.")
            print("Please, login in the pop up ............ and click on your profile after login on top right corner.")
            try:
                driver  = webdriver.Chrome(service=service, options=chrome_options)
                driver.get("https://www.reddit.com/login/")
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//span[normalize-space()="View Profile"]')
                    )
                )
                print("Logged In Successfully!")
                view_profile_span = WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//span[normalize-space()="View Profile"]')
                    )
                )
                username_span = view_profile_span.find_element(By.XPATH, 'following-sibling::span[1]')
                username = username_span.text.strip().removeprefix('u/')
                print("Your username:", username)

                time.sleep(10)

                cookies = driver.get_cookies()

                saveAuth(
                    platform_name='reddit',
                    username=username,
                    cookies=cookies
                )
            except:
                print("Time limit, exceeded! Please try again.")
        elif choice == "5":
            return
        else:
            print("Please enter a valid choice.")
            continue
        
        break