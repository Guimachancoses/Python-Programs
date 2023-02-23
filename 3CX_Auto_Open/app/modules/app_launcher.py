import os
import psutil
from time import sleep

def launch_app(app_path):
    try:
        os.startfile(app_path)
    except Exception as e:
        print(f"Error launching app: {e}")

def is_app_running(app_name):
    for proc in psutil.process_iter():
        try:
            if app_name in proc.name():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def check_and_launch_app(username=None):
    if not username:
        username = os.getlogin()
        app_name = "3CXDesktopApp.exe"
        app_path = rf'C:\Users\{username}\AppData\Local\Programs\3CXDesktopApp\3CXDesktopApp.exe'
        app_path2 = rf'C:\Users\{username}\AppData\Local\Programs\3CXDesktopApp\app\3CXDesktopApp.exe'
    if is_app_running(app_name):
        print("3CX Desktop App is already running")
    else:
        os.startfile(app_path)
        os.startfile(app_path2)
        print("3CX Desktop App has been launched")
        