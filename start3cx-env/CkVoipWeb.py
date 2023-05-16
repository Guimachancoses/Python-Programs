import os
import winreg
import sys
from time import sleep
import pygetwindow
import psutil


# URL a ser verificada
url = "https://garbuio.my3cx.com.br/webclient/#/people"


def is_app_running(url):
    # Verifica se o processo do Google Chrome está em execução
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'chrome.exe':
            # Obtém as janelas do Google Chrome em execução
            chrome_windows = pygetwindow.getWindowsWithTitle('garbuio.my3cx')
            for window in chrome_windows:
                if url in window.title:
                    return True
    return False


def start_if_not_running(app_path):
    if is_app_running(url):
        start_app(app_path)
    else:
        print("3CX Desktop App is already running")
        print("A página está aberta no Google Chrome.")


def start_app(app_path):
    try:
        os.startfile(app_path)
        print("3CX Desktop App has been launched")
    except OSError as e:
        print(f"Error starting app: {e}")

# Função se não está rodando, chamando a função start_app


def start_if_not_running(app_path):
    if is_app_running(url):
        start_app(app_path)

    else:
        print("3CX Desktop App is already running")
        print("A página está aberta no Google Chrome.")


def main(username=None):
    while True:
        # Verifica qual o nome do usuário está sendo executado o script
        if not username:
            username = os.getlogin()
            app_path = rf'C:\Users\guilhermemachado\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\apps do Chrome\3CX.lnk'

        # Nome do aplicativo a ser verificado
        app_name = "chrome.exe"

        try:
            start_if_not_running(app_path)

        except Exception as e:
            print(f"Error: {e}")

        sleep(15)


def add_to_startup():
    # Obtém o caminho para o arquivo Python
    python_exe = sys.executable
    script_path = os.path.abspath(__file__)

    # Define o nome da chave de registro
    key_name = "Verifique3CX"

    # Abre a chave do registro onde as tarefas agendadas são armazenadas
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE) as key:
        # Define o caminho completo para o script
        full_path = f'"{python_exe}" "{script_path}"'

        # Adiciona a chave de registro para iniciar o script no boot
        winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, full_path)


if __name__ == '__main__':
    # Adiciona o script aos serviços de inicialização do Windows
    add_to_startup()

    # Inicia o loop principal
    main()
