import os
import psutil
import shutil
from time import sleep

# Função verifica se a aplicação foi inserida no inicializar do Windows se não insere a mesma
def check_start_folder(path_app):
    try:
        # Define o caminho para a pasta de inicialização do Windows
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        print(startup_folder)

        # Define o caminho completo do arquivo que você deseja verificar
        arquivo = os.path.join(startup_folder, 'Check_v2.exe')
                
        # Verifica se o arquivo está presente na pasta de inicialização
        if os.path.exists(arquivo):
            print('O arquivo já está presente na pasta de inicialização.')
        else:
            # Copia o arquivo para a pasta de inicialização
            shutil.copy(path_app, startup_folder)
            print('O arquivo foi adicionado à pasta de inicialização.')
            
    except Exception as e:
        print('Ocorreu um erro ao adicionar o arquivo à pasta de inicialização:', e)
    
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
        
        # Caminho da Raiz do aplicativo de execução        
        path_app = r'\\sad01\DefaultPackageShare$\Installers\Check_v2.exe'
        
        try:
            check_start_folder(path_app)
            start_if_not_running(app_name, app_path)
            start_if_not_running(app_name, app_path2)
        except Exception as e:
            print(f"Error: {e}")
            # Você pode personalizar a mensagem de erro ou fazer algo diferente, dependendo da situação

        sleep(15)
        
if __name__ == '__main__':
    main()

