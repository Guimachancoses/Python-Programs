import traceback
import os
from datetime import datetime
from shutil import copyfile, rmtree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import zipfile
from time import sleep

# Função para logar no portal

def login(browser):
    try:
        browser.get("https://brado.multitransportador.com.br/Login?ReturnUrl=")
        login_field = browser.find_element(
            By.XPATH, '//*[@id="Usuario"]')
        password_field = browser.find_element(
            By.XPATH, '//*[@id="Senha"]')
        login_field.send_keys('56385-SP')
        password_field.send_keys('56385SP')
        browser.find_element(By.XPATH, '//*[@id="login-form"]/div[2]/div[3]/button') \
            .click()
        print("Logged in successfully!")
    except WebDriverException as e:
        print(f"Error during login: {traceback.format_exc()}")
    

def download_cte(browser):
    sleep(3)
    browser.get("https://brado.multitransportador.com.br/#CTe/ConsultaCTe")
    WebDriverWait(browser, 3).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="dropdownMenuButton1"]'))) \
        .click()
    WebDriverWait(browser, 3).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[2]/div/div/main/section/div[2]/div/div[2]/div[1]/div/div/ul/li[1]/a'))) \
        .click()
    
    
def wait_for_download(download_path, timeout=30):
    downloaded_file = None
    while timeout > 0:
        for file in os.listdir(download_path):
            if file.startswith("LoteXML") and file.endswith('.zip') and not file.endswith('.crdownload'):
                downloaded_file = os.path.join(download_path, file)
                break
        if downloaded_file:
            break
        sleep(1)
        timeout -= 1
    return downloaded_file

def copy_file(orig_dir, dest_dir):
    listdir = os.listdir(orig_dir)

    for arquivo in listdir:
        if arquivo.startswith("LoteXML") and arquivo.endswith(".zip"):
            origem = os.path.join(orig_dir, arquivo)

            # Adiciona a data e hora no formato desejado
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            novo_nome = f"LoteXML_{timestamp}.zip"

            destino = os.path.join(dest_dir, novo_nome)

            # Copia o arquivo ZIP para o destino
            copyfile(origem, destino)

            # Extrai o conteúdo do ZIP no destino
            with zipfile.ZipFile(destino, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    extracted_path = os.path.join(dest_dir, file_name)
                    
                    # Substituir o arquivo, se já existir
                    if os.path.exists(extracted_path):
                        if os.path.isdir(extracted_path):
                            rmtree(extracted_path)  # Remove diretórios
                        else:
                            os.remove(extracted_path)  # Remove arquivos

                # Extrair todos os arquivos do ZIP
                zip_ref.extractall(dest_dir)

            # Remove o arquivo ZIP original no destino
            os.remove(destino)

            # Remove o arquivo ZIP original na origem
            os.remove(origem)


def delete_file():
    orig_dir = fr"C:\Users\guilhermemachado\Downloads"

    listdir = os.listdir(orig_dir)

    for arquivo in listdir:
        if arquivo.startswith("LoteXML") and arquivo.endswith(".zip"):
            origem = os.path.join(orig_dir, arquivo)

            if os.path.exists(origem):
                os.remove(origem)
        


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
            # Set default wait time
            browser.implicitly_wait(5)

            login(browser)
            download_cte(browser)
            
            # Espere o download ser concluído
            download_path = fr"C:\Users\guilhermemachancoses\Downloads"
            downloaded_file = wait_for_download(download_path)
            
            if downloaded_file:
                print("Download zip concluído!")
            else:
                print("Erro ao fazer download do arquivo xls dentro do tempo limite.")
                
            browser.quit()
            # Definir o diretório de destino para o arquivo
            dest_dir = fr"Y:\BRADO"
            
            # Mover o arquivo para o servidor 
            try:
                max_attempts = 10
                wait_time = 300  # segundos
                attempt = 1   
                copy_file(download_path, dest_dir)
            except PermissionError as e:
                print(f"Erro ao copiar o arquivo: {e}")
                if attempt == max_attempts:
                    print(
                        "Não foi possível substituir o arquivo pois ele está sendo usado por outro processo.")
                    delete_file()
                else:
                    print(f"Tentando novamente em {wait_time} segundos...")
                    sleep(wait_time)
                    attempt += 1
            
                
        except Exception as e:
            print(f'Error: {e}')
            traceback.print_exc()
        finally:
            browser.quit()

    except Exception as e:
        print(f"Erro ao navegar para a página da web: {e}")
