import datetime
import traceback
import os
from shutil import copyfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from ChromeDriverSelenium import update_chrome_driver
from time import sleep


def wait_for_download(download_path, timeout=30):
    downloaded_file = None
    while timeout > 0:
        for file in os.listdir(download_path):
            if file.startswith("Fechamento_") and file.endswith('.xlsx') and not file.endswith('.crdownload'):
                downloaded_file = os.path.join(download_path, file)
                break
        if downloaded_file:
            break
        sleep(1)
        timeout -= 1
    return downloaded_file


def login(browser):
    browser.get("https://painel.tomticket.com")
    sleep(5)
    company_field = browser.find_element(
        By.XPATH, '/html/body/div/form/input[1]')
    login_field = browser.find_element(
        By.XPATH, '/html/body/div/form/input[2]')
    password_field = browser.find_element(
        By.XPATH, '/html/body/div/form/input[3]')
    company_field.send_keys('garbuio')
    login_field.send_keys('suporte@garbuio.com.br')
    password_field.send_keys('Sup0rt3@ERG')
    browser.find_element(By.XPATH, '/html/body/div/form/button') \
        .click()
    print("Logged in successfully!")


def navigate_to_download(browser):
    try:
        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="menu"]/ul/li[2]/a'))) \
            .click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="menu"]/ul/li[2]/ul/li[2]/a'))) \
            .click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="conteudo"]/div[5]/ng-view/div/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[4]/div/button'))) \
            .click()
        WebDriverWait(browser, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="conteudo"]/div[5]/ng-view/div/div/div[2]/div[4]/div[1]/table/tbody/tr[1]/td[4]/div/ul/li[1]/a'))) \
            .click()

        # Espere o download ser concluído
        download_path = fr"C:\Users\guilhermemachado\Downloads"
        downloaded_file = wait_for_download(download_path)

        if downloaded_file:
            print("Download xls concluído!")
        else:
            print("Erro ao fazer download do arquivo xls dentro do tempo limite.")
    except Exception as e:
        print(f'Error donwload xls: {e}')


def copy_file():
    orig_dir = fr"C:\Users\guilhermemachado\Downloads"
    dest_dir = fr"J:\Guilherme\FechamentoChamados"

    listdir = os.listdir(orig_dir)

    for arquivo in listdir:
        if arquivo.startswith("Fechamento_") and arquivo.endswith(".xlsx"):
            origem = os.path.join(orig_dir, arquivo)
            novo_nome = "FechamentoChamados.xlsx"
            destino = os.path.join(dest_dir, novo_nome)

            if os.path.exists(destino):
                os.remove(destino)

            copyfile(origem, destino)
            os.remove(origem)


def delete_file():
    orig_dir = fr"C:\Users\guilhermemachado\Downloads"

    listdir = os.listdir(orig_dir)

    for arquivo in listdir:
        if arquivo.startswith("Fechamento_") and arquivo.endswith(".xlsx"):
            origem = os.path.join(orig_dir, arquivo)

            if os.path.exists(origem):
                os.remove(origem)


def main():
    # Define as opções do navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')

    max_attempts = 10
    wait_time = 300  # segundos
    attempt = 1

    while attempt <= max_attempts:

        # Inicializa o driver do Chrome com as opções definidas
        try:
            update_chrome_driver()
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
                sleep(3)

                navigate_to_download(browser)
                copy_file()

                break
            except PermissionError as e:
                print(f"Erro ao copiar o arquivo: {e}")
            if attempt == max_attempts:
                print(
                    "Não foi possível substituir o arquivo pois ele está sendo usado por outro processo.")
                delete_file()
                break
            else:
                print(f"Tentando novamente em {wait_time} segundos...")
                sleep(wait_time)
                attempt += 1
        except Exception as e:
            print(f'Error: {e}')
            traceback.print_exc()
            break
        finally:
            browser.quit()


if __name__ == '__main__':
    main()
