import os
import psutil
import winreg
import sys
from time import sleep

# Função check se está rodando a aplicação
def is_app_running(app_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == app_name:
            return True
    return False

def start_app(app_path):
    try:
        os.startfile(app_path)
        print("3CX Desktop App has been launched")
    except OSError as e:
        print(f"Error starting app: {e}")

# Função se não está rodando, chamando a função start_app
def start_if_not_running(app_name, app_path):
    if not is_app_running(app_name):
        start_app(app_path)
           
    else:
        print("3CX Desktop App is already running")

def main(username=None):
    while True:
        # Verifica qual o nome do usuário está sendo executado o script
        if not username:
            username = os.getlogin()
            app_path = rf'C:\Users\{username}\AppData\Local\Programs\3CXDesktopApp\3CXDesktopApp.exe'
            app_path2 = rf'C:\Users\{username}\AppData\Local\Programs\3CXDesktopApp\app\3CXDesktopApp.exe'
        
        # Nome do aplicativo a ser verificado
        app_name = "3CXDesktopApp.exe"

        try:
            start_if_not_running(app_name, app_path)
            start_if_not_running(app_name, app_path2)
        except Exception as e:
            print(f"Error: {e}")
            # Você pode personalizar a mensagem de erro ou fazer algo diferente, dependendo da situação

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
