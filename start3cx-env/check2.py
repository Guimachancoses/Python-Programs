import os
import psutil
from time import sleep

def is_app_running(app_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == app_name:
            return True
    return False

def start_app(app_path):
    try:
        os.startfile(app_path)
    except OSError as e:
        print(f"Error starting app: {e}")
        # Você pode personalizar a mensagem de erro ou fazer algo diferente, dependendo da situação

def start_if_not_running(app_name, app_path):
    if not is_app_running(app_name):
        start_app(app_path)

def main():
    while True:
        app_name = "3CXDesktopApp.exe"
        app_path = r"C:\Users\stefancustodio\AppData\Local\Programs\3CXDesktopApp\3CXDesktopApp.exe"
        app_path_app = r"C:\Users\stefancustodio\AppData\Local\Programs\3CXDesktopApp\app\3CXDesktopApp.exe"

        try:
            start_if_not_running(app_name, app_path)
            start_if_not_running(app_name, app_path_app)
        except Exception as e:
            print(f"Error: {e}")
            # Você pode personalizar a mensagem de erro ou fazer algo diferente, dependendo da situação

        sleep(15)

if __name__ == "__main__":
    main()
