import datetime
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
# from modules.ChromeDriverSelenium import update_chrome_driver
from time import sleep


def login(browser):
    browser.get("https://cnw.vibraenergia.com.br/login/login.jsf")
    login_field = browser.find_element(
        By.XPATH, '/html/body/div/div[1]/div[2]/div[3]/div/form/div[1]/div[4]/div/input')
    password_field = browser.find_element(
        By.XPATH, '/html/body/div/div[1]/div[2]/div[3]/div/form/div[1]/div[6]/div/input')
    login_field.send_keys('CTELIMEIRA')
    password_field.send_keys('ctegarbuio4')
    browser.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div[3]/div/form/div[1]/div[7]/input') \
        .click()
    print("Logged in successfully!")


def navigate_to_queues(browser):
    try:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div[2]/div/div[1]/div/div[1]/button'))) \
            .click()
        WebDriverWait(browser, 3).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div[2]/ul/li[6]/a'))) \
            .click()
        WebDriverWait(browser, 3).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[2]/div[4]/div/div/div/div/input'))) \
            .click()
            
        print("Navigated to queues!")
        # Store the main window handle
        main_window_handle = browser.current_window_handle
        
        # Wait for a new window to appear
        WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
               
        # Switch to the new window
        for handle in browser.window_handles:
            if handle != main_window_handle:
                browser.switch_to.window(handle)
                break
        
        # Return the URL of the new window
        new_window_url = browser.current_url
        browser.switch_to.window(main_window_handle)
        return new_window_url
    except Exception as e:
        print(f'Error navigate in queue: {e}')


def navigate_to_extractCsv(browser):
    try:
        browser.find_element(
            'xpath','/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/div/table/tbody/tr/td/table[1]/tbody/tr/td[1]/div/div/div[5]').click()
        sleep(1)
        browser.find_element(
            'xpath', '/html/body/div[1]/table/tbody/tr[1]/td/div/div[1]/div[10]/div[2]').click()
        sleep(3)
        browser.find_element(
            'xpath', '/html/body/div[1]/table/tbody/tr[1]/td/div/div[1]/div[10]/div[2]').click()
        print("Extract successfully!")
    except Exception as e:
        print(f'Error Extract: {e}')
        traceback.print_exc()

def main():
    # Define as opções do navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')

    # Inicializa o driver do Chrome com as opções definidas
    try:
        # update_chrome_driver()
        try:
            browser = webdriver.Chrome(options=options)
        except WebDriverException as e:
            print(
                f"Ocorreu um erro ao iniciar o driver do Chrome após atualização: {e}")
            exit()

        try:
            now = datetime.datetime.now()
            print(now)

            # Set default wait time
            browser.implicitly_wait(5)

            login(browser)
            queue_url = navigate_to_queues(browser)
            sleep(10)

            if queue_url:
                browser.get(queue_url)
                navigate_to_extractCsv(browser)
                sleep(10)

        except Exception as e:
            print(f'Error: {e}')
            traceback.print_exc()
        finally:
            browser.quit()

    except Exception as e:
        print(f"Erro ao navegar para a página da web: {e}")
        
if __name__ == '__main__':
    main()

