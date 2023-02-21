import datetime
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def login(browser):
    browser.get("https://garbuio.my3cx.com.br/#/login")
    login_field = browser.find_element(By.XPATH, '//*[@id="content"]/login-component/div/div/form/div/div[1]/input')
    password_field = browser.find_element(By.XPATH, '//*[@id="content"]/login-component/div/div/form/div/div[2]/input')
    login_field.send_keys('5201')
    password_field.send_keys('L7jWz9qZGs')
    browser.find_element(By.XPATH, '//*[@id="content"]/login-component/div/div/form/button') \
        .click()
    print("Logged in successfully!")


def navigate_to_queues(browser):
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a')))
    browser.find_element(By.XPATH, '//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a') \
        .click()
    print("Navigated to queues!")


def force_user_on_queue(browser):
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "mc-select", " " ))]//i')))
        browser.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "mc-select", " " ))]//i') \
            .click()
        browser.find_element(By.XPATH, '//*[(@id = "btnStatus")]') \
            .click()
        WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div/div/div[2]/select[2]/option[3]')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/select[2]/option[3]') \
            .click()
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/button') \
            .click()
        print("User forced on queue successfully!")
    except Exception as e:
        print(f'Error forcing user on queue: {e}')
        traceback.print_exc()


def navigate_to_extensions(browser):
    browser.get('https://garbuio.my3cx.com.br/#/app/extensions')
    print("Navigated to extensions!")


def main():
    # Set browser - headless
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Update ChromeDriver version
    serv = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=serv, chrome_options=options)

    try:
        now = datetime.datetime.now()
        print(now)

        # Set default wait time
        browser.implicitly_wait(10)

        login(browser)
        while True:
            navigate_to_queues(browser)
            force_user_on_queue(browser)
            navigate_to_extensions(browser)
    except Exception as e:
        print(f'Error: {e}')
        traceback.print_exc()
    finally:
        browser.quit()


if __name__ == '__main__':
    main()
