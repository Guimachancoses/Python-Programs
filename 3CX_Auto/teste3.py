from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import datetime

def login(nav):
    try:
        nav.get("https://garbuio.my3cx.com.br/#/login")
        nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/div/div[1]/input').send_keys('5201')
        nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/div/div[2]/input').send_keys('L7jWz9qZGs')
        nav.find_element('xpath','//*[@id="content"]/login-component/div/div/form/button').click()
        WebDriverWait(nav, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="app-container"]'))) # espera até que a div "app-container" seja visível
    except:
        print("Erro durante o login.")
        raise

def navigate_to_queues(nav):
    try:
        nav.find_element(By.XPATH, '//*[@id="app-container"]/div[1]/div/div/nav/ul/app-nav-item[2]/a').click()
        WebDriverWait(nav, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="queues"]'))) # espera até que o botão "queues" esteja visível
    except:
        print("Erro ao navegar para a lista de filas.")
        raise

def navigate_to_status_dropdown(nav):
    try:
        nav.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "mc-select", " " ))]//i').click()
    except:
        print("Erro ao clicar na lista suspensa de status.")
        raise

def navigate_to_status_button(nav):
    try:
        nav.find_element(By.ID, 'btnStatus').click()
    except:
        print("Erro ao clicar no botão de alteração de status.")
        raise

def change_status(nav):
    try:
        WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "ng-valid-parse", " " ))]'))) # espera até que o botão de status esteja clicável
        nav.find_element(By.XPATH,'//*[contains(concat( " ", @class, " " ), concat( " ", "ng-valid-parse", " " ))]').click()
        WebDriverWait(nav, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/button'))) # espera até que o botão "Save" esteja clicável
        nav.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/button').click()
    except:
        print("Erro ao alterar o status.")
        raise

def navigate_to_extensions(nav):
    try:
        nav.get('https://garbuio.my3cx.com.br/#/app/extensions')
        WebDriverWait(nav, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="extensions"]'))) # espera até que a div "extensions" seja visível
    except:
        print("Erro ao navegar para a lista de ramais.")
        raise

def navigate_to_forced_queues(nav):
    try:
        navigate_to_queues(nav)
        navigate_to_status_dropdown(nav)
        navigate_to_status_button(nav)
        WebDriverWait(nav, 15).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/select[2]/option[3]'))) # espera até que a opção correta esteja visível na lista
        nav.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[1]/button').click()
        navigate_to_extensions(nav)
    except Exception as e:
        print(f"Erro ao navegar para fila forçada: {e}")

def navigate_to_change_status(nav):
    try:
        navigate_to_queues(nav)
        navigate_to_status_dropdown(nav)
        navigate_to_status_button(nav)
        change_status(nav)
        navigate_to_extensions(nav)
    except Exception as e:
        print(f"Erro ao navegar para mudar status: {e}")

def main():
    # Set navegador - oculto
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")

    # Atulizando a versão do DriverChrome
    serv = Service(ChromeDriverManager().install())
    nav = webdriver.Chrome(service=serv, chrome_options=options)

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print(now)

    try:
        login(nav)
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        nav.quit()
        exit()

    while True:
        try:
            if current_time != '13:30:00' and current_time != '07:00:00':
                navigate_to_forced_queues(nav)
            else:
                print(now)
                navigate_to_change_status(nav)
        except Exception as e:
            print(f"Erro ao executar ação: {e}")

        time.sleep(60) # espera 1 minuto até a próxima ação

        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")

if __name__ == "__main__":
    main()



