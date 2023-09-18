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
        By.XPATH, '//*[@id="content"]/login-component/div/div/form/div/div[1]/input')
    password_field = browser.find_element(
        By.XPATH, '//*[@id="content"]/login-component/div/div/form/div/div[2]/input')
    login_field.send_keys('5201')
    password_field.send_keys('L7jWz9qZGs')
    browser.find_element(By.XPATH, '//*[@id="content"]/login-component/div/div/form/button') \
        .click()
    print("Logged in successfully!")


def navigate_to_queues(browser):
    try:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a'))) \
            .click()
        print("Navigated to queues!")
    except Exception as e:
        print(f'Error navigate in queue: {e}')


def force_user_on_queue(browser):
    try:
        browser.find_element(
            'xpath', '//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a').click()
        sleep(1)
        browser.find_element(
            'xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "mc-select", " " ))]//i').click()
        browser.find_element('xpath', '//*[(@id = "btnStatus")]').click()
        sleep(15)
        browser.find_element(
            'xpath', '/html/body/div[1]/div/div/div/div[2]/select[2]/option[3]').click()
        sleep(1)
        browser.find_element(
            'xpath', '/html/body/div[1]/div/div/div/div[1]/button').click()
        sleep(1)
        browser.find_element(
            'xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "mc-select", " " ))]//i').click()
        print("User forced on queue successfully!")
    except Exception as e:
        print(f'Error forcing user on queue: {e}')
        traceback.print_exc()
        
def change_status(browser):
    try:
        userList = ['5020', '5022', '5051', '6009']
        input_field_xpath = '/html/body/div/div/div/div[2]/div[2]/div[2]/extension-list/div/div[2]/div/div[3]/div[1]/input'
        
        for user in userList:
            browser.find_element('xpath', input_field_xpath).clear()  # Limpa o campo de entrada
            browser.find_element('xpath', input_field_xpath).send_keys(user)  # Envia o número do ramal
            sleep(1)
            browser.find_element('xpath', '/html/body/div/div/div/div[2]/div[2]/div[2]/extension-list/div/div[2]/div/div[3]/table/tbody/tr/td[1]/label/i').click()  # Marca a caixa de seleção do usuário
            browser.find_element('xpath', '//*[(@id = "btnStatus")]').click()  # Clica no botão de status
            sleep(5)
            browser.find_element('xpath', '/html/body/div[1]/div/div/div/div[2]/select[1]/option[2]').click()  # Seleciona a opção 'disponível'
            sleep(1)
            browser.find_element('xpath', '/html/body/div[1]/div/div/div/div[1]/button').click()  # Fecha a janela de diálogo
            sleep(1)
            print(f"Ramal {user} forced on status successfully!")
    except Exception as e:
        print(f'Error forcing ramal {user} on status: {e}')
        traceback.print_exc()


def navigate_to_extensions(browser):
    browser.get('https://garbuio.my3cx.com.br/#/app/extensions')
    print("Navigated to extensions!")


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
                navigate_to_queues(browser)
                force_user_on_queue(browser)
                                
                # Verifique o horário atual
                current_time = now.time()
                print(current_time)
                if (current_time >= datetime.time(8, 0) and current_time <= datetime.time(12, 0)) or \
                   (current_time >= datetime.time(13, 0) and current_time <= datetime.time(18, 0)):
                    change_status(browser)
                    
                navigate_to_extensions(browser)
        except Exception as e:
            print(f'Error: {e}')
            traceback.print_exc()
        finally:
            browser.quit()

    except Exception as e:
        print(f"Erro ao navegar para a página da web: {e}")
