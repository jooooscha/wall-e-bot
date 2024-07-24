from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import json
from datetime import datetime, date, timedelta
import os, errno
from time import sleep
from random import uniform, shuffle, choice
import itertools
import tempfile
from collections import defaultdict

def login(driver):
    driver.get("https://www.spielerplus.de/de-li/site/login")
    mail_input = driver.find_element(By.XPATH, '//input[@id="loginform-email"]')
    mail_input.send_keys("joscha.loos@pm.me")
    pass_input = driver.find_element(By.XPATH, '//input[@id="loginform-password"]')
    pass_input.send_keys("qyGb0pRI9cp@hPNik8&/i3^HQbQtvhsE/$15=y&M#7!TcSQ@wNLS`4NoN3u1i6sw")

    login_button = driver.find_element(By.XPATH, '//form[@id="login-form"]//button[contains(@class, "button button--primary")]')
    login_button.click()

    sleep(2)

    select_ptsv = driver.find_element(By.XPATH, '//div[contains(@class, "select-team")]/a[following-sibling::div/h4[contains(text(), "PTSV MU20")]]')
    select_ptsv.click()
    print("Login successful")

def card(driver, card): # zusage: 0, unsicher 1, absage 2
    date = card.find_element(By.XPATH, './/div[@class="panel-heading-info"]')
    title = card.find_element(By.XPATH, './/div[@class="panel-heading-text"]')
    button_zusage = card.find_element(By.XPATH, './/button[contains(@class, "participation-button") and @title="Zugesagt"]')
    n_zusage = button_zusage.find_element(By.XPATH, './/div[@class="participation-number"]')
    button_unsicher = card.find_element(By.XPATH, './/button[contains(@class, "participation-button") and @title="Unsicher"]')
    n_unsicher = button_unsicher.find_element(By.XPATH, './/div[@class="participation-number"]')
    button_absage = card.find_element(By.XPATH, './/button[contains(@class, "participation-button") and @title="Absagen / Abwesend"]')
    n_absage = button_absage.find_element(By.XPATH, './/div[@class="participation-number"]')

    print("date:", date.text)
    print("title:", title.text)
    print("n_zusage:", n_zusage.text)
    print("n_unsicher:", n_unsicher.text)
    print("n_absage:", n_absage.text)

    print(f"Termin am {date.text.replace("\n", "")} ({title.text})")
    print(f"Aktuell: Zusage: {n_zusage.text}, Absage: {n_absage.text}, Unsicher: {n_unsicher.text}")
    print("Du kannst Zusagen (0), unsicher (1), absagen (2)")
    action = input()
    action = int(action.strip())

    sleep(2)

    match action:
        case 0:
            driver.execute_script("arguments[0].click();", button_zusage)
            sleep(2)
            unsicher_input = driver.find_element(By.XPATH, '//input[@id="participation-reason"]')
            unsicher_input.clear()
        case 1:
            driver.execute_script("arguments[0].click();", button_unsicher)
            sleep(2)
            unsicher_input = driver.find_element(By.XPATH, '//input[@id="participation-reason"]')
            unsicher_input.send_keys("Weiß noch nicht ob ich in Aachen bin")
        case 2:
            driver.execute_script("arguments[0].click();", button_absage)
            sleep(2)
            absage_input = driver.find_element(By.XPATH, '//input[@id="participation-reason"]')
            absage_input.send_keys("Bin nicht in Aachen :(")

    sleep(2)
    submit_button = driver.find_element(By.XPATH, '//button[contains(@class, "submit-participation")]')
    driver.execute_script("arguments[0].click();", submit_button)


def fetch(driver):
    list_events = driver.find_elements(By.XPATH, '//div[@class="dashboard dashboard--home"]//div[@class="list event"]')

    for i, event in enumerate(list_events):
        if i == 0:
            continue
        card(driver, event)
        input()

def main():

    options = Options()
    #  options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    login(driver)
    data = fetch(driver)
    print("data:", data)

    driver.quit()

    #  db.close()

if __name__ == "__main__":
    main()
