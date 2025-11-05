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
    browser.get("https://garbuio.my3cx.com.br/#/login")
    login_field = browser.find_element(
        By.XPATH, '//*[@id="loginInput"]')
    password_field = browser.find_element(
        By.XPATH, '//*[@id="passwordInput"]')
    login_field.send_keys('5201')
    password_field.send_keys('L7jWz9qZGs')
    browser.find_element(By.XPATH, '//*[@id="submitBtn"]') \
        .click()
    print("Logged in successfully!")

def find_all_user_status(browser):
    try:
        # Navegar pro menu
        WebDriverWait(browser, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a'))
        ).click()
        print("Navigated to queues!")

        # Esperar e capturar todos os indicadores com as classes desejadas
        status_indicators = WebDriverWait(browser, 5).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 "//i[contains(@class,'status-indicator') and "
                 "("
                     "contains(@class,'out_of_office') or "
                     "contains(@class,'custom2') or "
                     "contains(@class,'away')"
                 ")"
                 "]")
            )
        )

        print(f"Found {len(status_indicators)} status indicators matching criteria.")
        return status_indicators

    except Exception as e:
        print(f"Error: {e}")
        return []

def force_user_on_queue(browser):
    try:
        # Clica em mais opções
        browser.find_element(
            'xpath', '/html/body/app/div/div/div/ng-component/div/layout/div/div/div[2]/ng-component/layout-type2/div/div/people-list/ul/people-tile/span/div/a[5]').click()
        sleep(1)
        # clica em definiir status
        element = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'dropdown-item')]//span[normalize-space()='Definir status']"))
        )
        element.click()
        sleep(1)
        # clica na caixa de opções
        browser.find_element(
            'xpath', '/html/body/modal-container/div[2]/div/ng-component/app-modal-dialog/div[2]/field-select/field-wrapper/div[1]/div[2]/ng-select/div/div/div[3]').click()
        sleep(1)
        # seleciona disponível
        browser.find_element(
            'xpath', '/html/body/modal-container/div[2]/div/ng-component/app-modal-dialog/div[2]/field-select/field-wrapper/div[1]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[1]').click()
        sleep(1)
        # clica em salvar
        browser.find_element(
            'xpath', '/html/body/modal-container/div[2]/div/ng-component/app-modal-dialog/div[3]/span/button').click()
        print("User forced on status successfully!")
    except Exception as e:
        print(f'Error forcing user on queue: {e}')
        traceback.print_exc()


def select_user(browser):
    try:
        userList = ['1021',
                    '3006',
                    '5020','5024','5030','5047','5051','5052','5053','5054','5055','5066','5069','5071','5075','5077','5078','5080','5082','5086','5091',
                    '5304',
                    '6009','6010','6015']
        input_field_xpath = '//*[@id="inputSearch"]'

        for user in userList:
            # Limpa o campo de entrada
            browser.find_element('xpath', input_field_xpath).clear()
            browser.find_element('xpath', input_field_xpath).send_keys(
                user)  # Envia o número do ramal
            sleep(1)
            print(f"Ramal {user} find user successfully!")
            force_user_on_queue(browser)
    except Exception as e:
        print(f'Error forcing ramal {user} on status: {e}')
        traceback.print_exc()


def main():
    # Define as opções do navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')

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
            # Set default wait time
            browser.implicitly_wait(5)

            login(browser)
            while True:
                now = datetime.datetime.now()
                #find_all_user_status(browser)
                #force_user_on_queue(browser)

                # Verifique o horário atual entre às 08:00 e 12 horas
                current_time = now.time()
                print(current_time)
                if (current_time >= datetime.time(8, 0) and current_time <= datetime.time(12, 0)) or \
                   (current_time >= datetime.time(13, 0) and current_time <= datetime.time(22, 0)):
                    select_user(browser)
                
        except Exception as e:
            print(f'Error: {e}')
            traceback.print_exc()
        finally:
            browser.quit()

    except Exception as e:
        print(f"Erro ao navegar para a página da web: {e}")
