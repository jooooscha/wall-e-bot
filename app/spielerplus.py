from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import datetime, date, timedelta
from time import sleep

def wait():
    sleep(3)

def click(driver, button):
    driver.execute_script("arguments[0].click();", button)

def login(driver):
    driver.get("https://www.spielerplus.de/de-li/site/login")
    mail_input = driver.find_element(By.XPATH, '//input[@id="loginform-email"]')
    mail_input.send_keys("joscha.loos@pm.me")
    pass_input = driver.find_element(By.XPATH, '//input[@id="loginform-password"]')
    pass_input.send_keys("qyGb0pRI9cp@hPNik8&/i3^HQbQtvhsE/$15=y&M#7!TcSQ@wNLS`4NoN3u1i6sw")

    login_button = driver.find_element(By.XPATH, '//form[@id="login-form"]//button[contains(@class, "button button--primary")]')
    click(driver, login_button)

    wait()

    select_ptsv = driver.find_element(By.XPATH, '//div[contains(@class, "select-team")]/a[following-sibling::div/h4[contains(text(), "PTSV MU20")]]')
    click(driver, select_ptsv)
    print("Login successful")

class Card:
    def __init__(self, driver, card):
        self.driver = driver
        self.date = card.find_element(By.XPATH, './/div[@class="panel-heading-info"]')
        self.title = card.find_element(By.XPATH, './/div[@class="panel-heading-text"]')
        self.button_zusage = card.find_element(By.XPATH, './/button[contains(@class, "participation-button") and @title="Zugesagt"]')
        self.n_zusage = self.button_zusage.find_element(By.XPATH, './/div[@class="participation-number"]')
        self.button_unsicher = card.find_element(By.XPATH, './/button[contains(@class, "participation-button") and @title="Unsicher"]')
        self.n_unsicher = self.button_unsicher.find_element(By.XPATH, './/div[@class="participation-number"]')
        self.button_absage = card.find_element(By.XPATH, './/button[contains(@class, "participation-button") and @title="Absagen / Abwesend"]')
        self.n_absage = self.button_absage.find_element(By.XPATH, './/div[@class="participation-number"]')

        # init load participants

        self.participants_button = card.find_element(By.XPATH, './/button[contains(@class, "participants-button")]')
        self.driver.execute_script("arguments[0].click();", self.participants_button)

        wait()

        #  x = driver.find_element(By.XPATH, '//div[@class="modal-dialog "]//div[@id="lists"]') # note the space after modal-dialog
        groups = driver.find_elements(By.XPATH, '//div[@id="lists"]/div[@class="participation-list"]') # groups of people: zugesagt, unsicher, ...
        for group in groups:
            header = group.find_element(By.XPATH, './div[@class="participation-list-header"]')
            header_text = header.text.split("\n")[0]

            match header_text:
                case "Noch nicht zu/abgesagt":
                    print(f"Fetching names from {header_text}")
                    names = group.find_elements(By.XPATH, './/div[@class="participation-list-user-name"]')
                    self.pending = [ n.text for n in names ]
                case _: # todo
                    print(f"Skipping group {header_text}")

    def info(self):
        return {
            "date": self.date.text.replace("\n", " "),
            "title": self.title.text,
            "n_zusage": self.n_zusage.text,
            "n_unsicher": self.n_unsicher.text,
            "n_absage": self.n_absage.text,
        }


    def get_buttons(self):
        return self.button_zusage, self.button_unsicher, self.button_absage

    def get_pending(self):
        return self.pending

def fetch_next_event():
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)

    login(driver)
    wait()

    next_event = driver.find_elements(By.XPATH, '//div[@class="dashboard dashboard--home"]//div[@class="list event"]')[0]

    wait()

    card = Card(driver, next_event)

    info = card.info()
    info["pending"] = card.get_pending()

    driver.quit()

    #  print(f"Termin am {info['date'].replace("\n", "")} ({info['title']})")
    #  print(f"Aktuell: Zusage: {info['n_zusage']}, Absage: {info['n_absage']}, Unsicher: {info['n_unsicher']}")
    #  text = f"Currently pending {card.get_pending()}"
    return info

#  def card(driver, card): # zusage: 0, unsicher 1, absage 2

#      card = Card(driver, card)

#      button_zusage, button_unsicher, button_absage = card.get_buttons()

#      print("Du kannst Zusagen (0), unsicher (1), absagen (2)")
#      action = input()
#      action = int(action.strip())

#      wait()

#      match action:
#          case 0:
#              driver.execute_script("arguments[0].click();", button_zusage)
#              wait()
#              unsicher_input = driver.find_element(By.XPATH, '//input[@id="participation-reason"]')
#              unsicher_input.clear()
#          case 1:
#              driver.execute_script("arguments[0].click();", button_unsicher)
#              wait()
#              unsicher_input = driver.find_element(By.XPATH, '//input[@id="participation-reason"]')
#              unsicher_input.send_keys("Weiß noch nicht ob ich in Aachen bin")
#          case 2:
#              driver.execute_script("arguments[0].click();", button_absage)
#              wait()
#              absage_input = driver.find_element(By.XPATH, '//input[@id="participation-reason"]')
#              absage_input.send_keys("Bin nicht in Aachen :(")

#      wait()
#      submit_button = driver.find_element(By.XPATH, '//button[contains(@class, "submit-participation")]')
#      #  driver.execute_script("arguments[0].click();", submit_button)

