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

def fetch(driver):
    driver.get("https://www.spielerplus.de/de-li/site/login")
    input()

def main():

    print(f"{i+1}/{len(dates)}")

    options = Options()
    options.add_argument("-headless")

    #  profile = webdriver.FirefoxProfile()
    #  profile.set_preference("general.useragent.override", user_agent)
    #  options.profile = profile

    driver = webdriver.Firefox(options=options)

    connections = fetch(driver)


    #  db.insert_data(check_date, connection_date, connections, user_agent)

    #  t = uniform(1,5)
    #  print(f"Waiting {t} seconds")
    #  sleep(t)
    driver.quit()

    db.close()

if __name__ == "__main__":
    main()
