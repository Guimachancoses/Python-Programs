import io
import urllib.request
import zipfile
import os
import platform
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

def update_edge_driver():
    try:
        # Verifica o sistema operacional
        system = platform.system()
        if system == 'Windows':
            edgedriver_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
            response = urllib.request.urlopen(edgedriver_url)
            latest_version = response.read().decode('utf-8')
            edgedriver_url = f"https://msedgedriver.azureedge.net/{latest_version}/edgedriver_win64.zip"
        elif system == 'Linux':
            edgedriver_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
            response = urllib.request.urlopen(edgedriver_url)
            latest_version = response.read().decode('utf-8')
            edgedriver_url = f"https://msedgedriver.azureedge.net/{latest_version}/edgedriver_linux64.zip"
        elif system == 'Darwin':
            edgedriver_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
            response = urllib.request.urlopen(edgedriver_url)
            latest_version = response.read().decode('utf-8')
            edgedriver_url = f"https://msedgedriver.azureedge.net/{latest_version}/edgedriver_mac64.zip"
        else:
            raise ValueError("Sistema operacional não suportado")

        # Download e extração do arquivo zip
        response = urllib.request.urlopen(edgedriver_url)
        zip_file = zipfile.ZipFile(io.BytesIO(response.read()))
        zip_file.extractall()

        # Encontra o arquivo executável do driver
        executable = ''
        for file in os.listdir():
            if 'msedgedriver' in file:
                executable = file
                break

        # Move o arquivo executável para o PATH do sistema
        if executable:
            os.chmod(executable, 0o755)
            os.replace(executable, f"/usr/local/bin/{executable}")
            print(f"Edge Driver Selenium atualizado com sucesso para a versão {executable}")
        else:
            print("Não foi possível encontrar o arquivo executável do Edge Driver Selenium")
    except (ValueError, urllib.error.URLError, zipfile.BadZipFile, OSError) as e:
        print(f"Ocorreu um erro ao atualizar o Edge Driver Selenium: {str(e)}")

# Define as opções do navegador
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_argument('--headless')

# Inicializa o driver do Edge com as opções definidas
try:
    driver = webdriver.Edge(options=options)
except WebDriverException as e:
    print(f"Ocorreu um erro ao inicializar o driver do Edge: {str(e)}")

# Navega para uma página da web
try:
    driver.get("https://www.google.com")
except WebDriverException as e:
    print(f"Ocorreu um erro ao navegar para a página da web: {str(e)}")

# Imprime o título da página
try:
    print(driver.title)
except WebDriverException as e:
    print(f"Ocorreu um erro ao imprimir o título da página: {str(e)}")

# Fecha o navegador
try:
    driver.quit()
except WebDriverException as e:
    print(f"Ocorreu um erro ao imprimir o título da página: {str(e)}")
    pass

