from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
import schedule

# preparing alerts (quick 'n dirty right now)
url = "https://discord.com/api/webhooks/create/your-own-h00ka"
stub_message = f"BTC monke(s) found new home!"
embed = {
    "description": stub_message,
    "title": "ATTENTION PLEASE!"
    }
data = {
    "embeds": [
        embed
        ],
}
headers = {
"Content-Type": "application/json"
}

# Path Chrome-Webdriver
chrome_driver_path = 'chromedriver.exe'

# URL where to scrape
url = 'https://ordinalsbot.com/mint/btc-artsy-monke'

def ord_scraper():
    # Start Chrome
    driver = webdriver.Chrome(chrome_driver_path)
    driver.minimize_window()
    driver.get(url)

    # wait for up to 10 seconds for the element to be visible
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.detail")))

    # get the text of the element
    available_count = int(element.text.split(': ')[-1].split(' ')[0])
    print(f'Available Monke: {available_count}')

    sleep(3)
    print('Going into endless loop')
    try:
        while True:
            sleep(10)
            elements = driver.find_element(By.CSS_SELECTOR, "p.detail")
            new_available_count = int(elements.text.split(': ')[-1].split(' ')[0])
            print('doing something here')
            if new_available_count != available_count:
                print(f'Available Monke: {new_available_count}')
                available_count = new_available_count
                result= requests.post(url, json=data, headers=headers)
                if 200 <= result.status_code < 300:
                    print(f"Webhook sent {result.status_code}")
                else:
                    print(f"Not sent with {result.status_code}, response:\n{result.json()}")
    except:
        print("Something went wrong, send the highly trained apes!")
    sleep(10)


# schedule it
ord_scraper()
schedule.every(15).seconds.do(ord_scraper)

while True:
    try:
        schedule.run_pending()
        sleep(15)
    except:
        print('Internet Problem? Retrying in a minute...')
        sleep(60)
