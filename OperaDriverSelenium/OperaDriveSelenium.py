import urllib.request
import zipfile
import os
import platform
from selenium import webdriver

def update_opera_driver():
    # Verifica o sistema operacional
    system = platform.system()
    if system == 'Windows':
        operadriver_url = "https://github.com/operasoftware/operachromiumdriver/releases/latest/download/operadriver_win64.zip"
    elif system == 'Linux':
        operadriver_url = "https://github.com/operasoftware/operachromiumdriver/releases/latest/download/operadriver_linux64.zip"
    elif system == 'Darwin':
        operadriver_url = "https://github.com/operasoftware/operachromiumdriver/releases/latest/download/operadriver_mac64.zip"
    else:
        raise ValueError("Sistema operacional não suportado")

    # Download e extração do arquivo zip
    response = urllib.request.urlopen(operadriver_url)
    zip_file = zipfile.ZipFile(io.BytesIO(response.read()))
    zip_file.extractall()

    # Encontra o arquivo executável do driver
    executable = ''
    for file in os.listdir():
        if 'operadriver' in file:
            executable = file
            break

    # Move o arquivo executável para o PATH do sistema
    if executable:
        os.chmod(executable, 0o755)
        os.replace(executable, f"/usr/local/bin/{executable}")
        print(f"Opera Driver Selenium atualizado com sucesso para a versão {executable}")
    else:
        print("Não foi possível encontrar o arquivo executável do Opera Driver Selenium")
        

# Define as opções do navegador
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")
options.add_argument('--headless')

# Inicializa o driver do Opera com as opções definidas
driver = webdriver.Opera(options=options)

# Navega para uma página da web
driver.get("https://www.google.com")

# Imprime o título da página
print(driver.title)

# Fecha o navegador
driver.quit()
