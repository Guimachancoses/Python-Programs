import io
import os
import platform
import re
import urllib.request
import zipfile

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def update_chrome_driver():
    try:
        # Verifica o sistema operacional
        system = platform.system()
        if system == 'Windows':
            chromedriver_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            response = urllib.request.urlopen(chromedriver_url)
            latest_version = response.read().decode('utf-8')
            chromedriver_url = f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_win32.zip"
        elif system == 'Linux':
            chromedriver_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            response = urllib.request.urlopen(chromedriver_url)
            latest_version = response.read().decode('utf-8')
            chromedriver_url = f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_linux64.zip"
        elif system == 'Darwin':
            chromedriver_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            response = urllib.request.urlopen(chromedriver_url)
            latest_version = response.read().decode('utf-8')
            chromedriver_url = f"https://chromedriver.storage.googleapis.com/{latest_version}/chromedriver_mac64.zip"
        else:
            raise ValueError("Sistema operacional não suportado")

        # Verifica a versão do Chrome
        chrome_version = re.search(r"\d+\.\d+\.\d+\.\d+", webdriver.Chrome(executable_path='chromedriver').capabilities['browserVersion']).group()
        if latest_version.split('.')[0] > chrome_version.split('.')[0]:
            raise ValueError("Versão do ChromeDriver incompatível com a versão do Chrome instalada")

        # Download e extração do arquivo zip
        response = urllib.request.urlopen(chromedriver_url)
        zip_file = zipfile.ZipFile(io.BytesIO(response.read()))
        zip_file.extractall()

        # Encontra o arquivo executável do driver
        executable = ''
        for file in os.listdir():
            if 'chromedriver' in file:
                executable = file
                break

        if not executable:
            raise FileNotFoundError("Arquivo executável do Chrome Driver Selenium não encontrado")

        # Move o arquivo executável para o PATH do sistema
        os.chmod(executable, 0o755)
        path = '/usr/local/bin/'
        if not os.path.isdir(path):
            os.makedirs(path)
        os.replace(executable, f"{path}{executable}")
        print(f"Chrome Driver Selenium atualizado com sucesso para a versão {executable}")

    except (urllib.error.URLError, zipfile.BadZipFile, ValueError, FileNotFoundError) as e:
        print(f"Ocorreu um erro ao atualizar o Chrome Driver Selenium: {e}")
        return

'''
# Define as opções do navegador
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_argument('--headless')

# Inicializa o driver do Chrome com as opções definidas
try:
    update_chrome_driver()
    try:
        browser = webdriver.Chrome(options=options)
    except WebDriverException as e:
        print(f"Ocorreu um erro ao iniciar o driver do Chrome após atualização: {e}")
        exit()

    # Navega para uma página da web
    browser.get("https://www.google.com")

    # Imprime o título da página
    print(browser.title)

except Exception as e:
    print(f"Erro ao navegar para a página da web: {e}")
finally:
    # Fecha o navegador
    try:
        browser.quit()
    except NameError:
        pass  # Não foi possível inicializar o driver, não precisa fechar o navegador
'''