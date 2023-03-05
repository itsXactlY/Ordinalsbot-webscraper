from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
import schedule

# preparing alerts (quick 'n dirty right now)
hook = 'https://discord.com/api/webhooks/create/your-own-h00ka'

def send_webhook_message(new_amount):
    message = f'BTC monke(s) found new home! {new_amount} left alone...'
    req = requests.post(hook, json={'content': message})
    if 200 <= req.status_code < 300:
        print(f"Webhook sent {req.status_code}")
    else:
        print(f"Not sent with {req.status_code}, response:\n{req.json()}")


# Path Chrome-Webdriver
chrome_driver_path = 'chromedriver.exe'

# URL where to scrape
scrape_url = 'https://ordinalsbot.com/mint/btc-artsy-monke'

def ord_scraper():
    # Start Chrome
    driver = webdriver.Chrome(chrome_driver_path)
    driver.minimize_window()
    driver.get(scrape_url)

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
            sleep(1.25)
            elements = driver.find_element(By.CSS_SELECTOR, "p.detail")
            new_available_count = int(elements.text.split(': ')[-1].split(' ')[0])
            print(f'Available Monke: {available_count}')
            if new_available_count != available_count:
                available_count = new_available_count
                send_webhook_message(new_available_count)

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
