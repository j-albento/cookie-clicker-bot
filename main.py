from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, value="cookie")
money = driver.find_element(By.ID, value="money")

store_items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in store_items]

timeout = time.time() + 5
five_min = time.time() + (60 * 5)

while True:
    cookie.click()

    # Every 5 seconds
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store div b")
        item_prices = []

        for price in all_prices:
            price_text = price.text

            if price_text != "":
                item_cost = int(price_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(item_cost)

        money_text = money.text
        money_text = money_text.replace(",", "")
        cookie_count = int(money_text)

        upgrades = {}
        for n in range(len(item_prices)):
            upgrades[item_prices[n]] = item_ids[n]

        affordable_upgrades = {}
        for cost, item_id in upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = item_id

        most_expensive_upgrade = max(affordable_upgrades)
        most_expensive_upgrade_id = affordable_upgrades[most_expensive_upgrade]

        most_expensive_item = driver.find_element(By.ID, value=most_expensive_upgrade_id)
        most_expensive_item.click()

        timeout = time.time() + 5

        if time.time() > five_min:
            cookies_per_second = driver.find_element(By.ID, value="cps").text
            print(cookies_per_second)
