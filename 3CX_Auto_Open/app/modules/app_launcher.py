import os
import psutil
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
        if not username:
            username = os.getlogin()
            app_path = rf'C:\Users\{username}\AppData\Local\Programs\3CXDesktopApp\3CXDesktopApp.exe'
            app_path2 = rf'C:\Users\{username}\AppData\Local\Programs\3CXDesktopApp\app\3CXDesktopApp.exe'
        
        app_name = "3CXDesktopApp.exe"        

        try:
            start_if_not_running(app_name, app_path)
            start_if_not_running(app_name, app_path2)
        except Exception as e:
            print(f"Error: {e}")
            # Você pode personalizar a mensagem de erro ou fazer algo diferente, dependendo da situação

        sleep(15)
        
        