from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
import schedule

# URL where to scrape
mint_url = 'https://ordinalsbot.com/mint/btc-artsy-monke'

# Webhook URL (Discod, Telegram, Weather Forecast...)
webhook_url = 'https://discord.com/api/webhooks/create/your-own-h00k'


def send_webhook_message(new_minted_monke, new_amount):
    message = f'{new_minted_monke} BTC Monke(s) minted and found a new home! {new_amount} Monke left alone...'
    req = requests.post(webhook_url, json={'content': message})
    if 200 <= req.status_code < 300:
        print(f"Webhook sent {req.status_code}")
    else:
        print(f"Not sent with {req.status_code}, response:\n{req.json()}")

def ord_scraper():
    try:
        # Path Chrome-Webdriver
        chrome_driver_path = 'chromedriver.exe'
        # Start Chrome
        driver = webdriver.Chrome(chrome_driver_path)
        driver.minimize_window()
        driver.get(mint_url)

        # wait for up to 10 seconds for the element to be visible
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.detail")))
        # get the text of the element
        available_count = int(element.text.split(': ')[-1].split(' ')[0])
        print(f'Available Monke: {available_count}')
        
        while True:
            sleep(30)
            '''
            ^^^^^^^^^^
            dont go ham on it until we can get needed details via API
            '''
            print('next check in 30')
            # fetching details
            elements = driver.find_element(By.CSS_SELECTOR, "p.detail")
            new_available_count = int(elements.text.split(': ')[-1].split(' ')[0])
            new_minted_monke = new_available_count - available_count
            
            if new_minted_monke > 0:
                print(f'{new_minted_monke} new Monke(s) minted! Total available: {new_available_count}')
                available_count = new_available_count
                send_webhook_message(new_minted_monke, new_available_count)

    except:
        print("Something went wrong - send the highly trained apes to halp!")

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
