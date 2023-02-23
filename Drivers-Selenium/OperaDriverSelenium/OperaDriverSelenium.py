import io
import urllib.request
import zipfile
import os
import platform
from selenium import webdriver

DRIVER_NAME = 'operadriver'

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

    # Verifica se o arquivo executável já está presente no sistema
    executable = None
    for path in os.get_exec_path():
        if os.path.isfile(os.path.join(path, DRIVER_NAME)):
            executable = os.path.join(path, DRIVER_NAME)
            break

    # Se o arquivo executável não estiver presente, faz o download e a extração
    if not executable:
        try:
            response = urllib.request.urlopen(operadriver_url)
            zip_file = zipfile.ZipFile(io.BytesIO(response.read()))
            zip_file.extractall()
        except Exception as e:
            print(f"Erro ao baixar ou extrair o arquivo: {e}")
            return

        # Encontra o arquivo executável do driver
        for file in os.listdir():
            if DRIVER_NAME in file:
                executable = file
                break

        # Move o arquivo executável para o PATH do sistema
        if executable:
            try:
                os.chmod(executable, 0o755)
                for path in os.get_exec_path():
                    os.replace(executable, os.path.join(path, DRIVER_NAME))
                print(f"Opera Driver Selenium atualizado com sucesso para a versão {executable}")
            except Exception as e:
                print(f"Erro ao mover o arquivo para o PATH do sistema: {e}")
        else:
            print("Não foi possível encontrar o arquivo executável do Opera Driver Selenium")
    else:
        print(f"O arquivo executável do Opera Driver Selenium já está presente no sistema ({executable})")

try:
    # Define as opções do navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')

    # Verifica se o driver está atualizado e, se necessário, faz o download e a instalação
    update_opera_driver()

    # Inicializa o driver do Opera com as opções definidas
    browser = webdriver.Opera(options=options)

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

