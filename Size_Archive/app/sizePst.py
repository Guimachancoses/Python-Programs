import os
import sys
import winreg
import configparser
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# função para adicionar no agendamento do iniciar do windows


def add_to_startup():
    # Obtém o caminho para o arquivo Python
    python_exe = sys.executable
    script_path = os.path.abspath(__file)

    # Define o nome da chave de registro
    key_name = "VerifiquePST"

    # Abre a chave do registro onde as tarefas agendadas são armazenadas
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE) as key:
        # Define o caminho completo para o script
        full_path = f'"{python_exe}" "{script_path}"'

        # Adiciona a chave de registro para iniciar o script no boot
        winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, full_path)

# obter o tamanho do arquivo


def obter_tamanho_arquivo_em_gb(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        tamanho_bytes = os.path.getsize(caminho_arquivo)
        tamanho_gb = tamanho_bytes / (1024 ** 3)  # 1 gigabyte = 1024^3 bytes
        return tamanho_gb
    else:
        return None

# formatar o tamanho de bytes oara gigabytes


def formatar_tamanho_em_gb(tamanho_gb):
    if tamanho_gb is not None:
        return f"{tamanho_gb:.2f} GB"
    else:
        return "Arquivo não encontrado"

# verificar se o tamanho exece o maximo estábelecido


def verificar_tamanho_pst(caminho_arquivo):
    tamanho_gb = obter_tamanho_arquivo_em_gb(caminho_arquivo)
    if tamanho_gb is not None:
        if tamanho_gb > 40:
            return "Favor verificar o arquivo PST, compacte-o ou crie um novo!"
    return None

# Função para obter o caminho do arquivo PST


def obter_caminho_arquivo_pst():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'PST' in config and 'Path' in config['PST']:
        return config['PST']['Path']
    else:
        return None

# Função para configurar o caminho do arquivo PST


def configurar_caminho_arquivo_pst(caminho):
    config = configparser.ConfigParser()
    if 'PST' not in config:
        config['PST'] = {}
    config['PST']['Path'] = caminho
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# função para salvar o caminho do arquivo PST dentro do "config.ini"


def salvar_caminho(janela_config, caminho_edit):
    caminho_arquivo = caminho_edit.text()
    configurar_caminho_arquivo_pst(caminho_arquivo)
    janela_config.close()


def abrir_dialogo_selecao_arquivo(caminho_edit):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    caminho_arquivo, _ = QFileDialog.getOpenFileName(
        None, "Selecionar arquivo PST", "", "Arquivos PST (*.pst);;Todos os arquivos (*)", options=options)

    try:
        if caminho_arquivo:
            caminho_edit.setText(caminho_arquivo)
    except Exception as e:
        print(f"Erro ao definir o caminho no campo de edição: {e}")

# função para pedir o caminho absouluto do arquivo PST, caso não exista no arquivo "config.ini"


def criar_janela_configuracao_caminho():
    janela_config = QMainWindow()
    janela_config.setWindowTitle("Configurar Caminho PST")
    janela_config.setWindowIcon(QIcon(
        fr"C:\Users\guilhermemachado\Documents\GitHub\Python-Programs\Size_Archive\alien.ico"))
    janela_config.setGeometry(100, 100, 400, 150)

    central_widget = QWidget(janela_config)
    janela_config.setCentralWidget(central_widget)

    layout = QVBoxLayout()
    caminho_label = QLabel("Caminho do arquivo PST:")

    caminho_edit = QLineEdit()  # Crie um objeto QLineEdit separado para o campo de edição
    selecionar_arquivo_button = QPushButton("Selecionar Arquivo")

    selecionar_arquivo_button.clicked.connect(
        lambda: abrir_dialogo_selecao_arquivo(caminho_edit))

    salvar_button = QPushButton("Salvar")
    salvar_button.clicked.connect(
        lambda: salvar_caminho(janela_config, caminho_edit))

    layout.addWidget(caminho_label)
    layout.addWidget(caminho_edit)
    layout.addWidget(selecionar_arquivo_button)
    layout.addWidget(salvar_button)

    central_widget.setLayout(layout)

    janela_config.show()
    return janela_config


def main():
    # Verifica se o arquivo de configuração já possui um caminho armazenado
    caminho_arquivo = obter_caminho_arquivo_pst()

    if caminho_arquivo is None:
        appin = QApplication(sys.argv)
        # Se o caminho não estiver armazenado, abre a janela de configuração
        janela_config = criar_janela_configuracao_caminho()
        janela_config(sys.exit(appin.exec_()))
        
    # O restante do seu código permanece o mesmo
    while True:
        try:
            tamanho_gb = obter_tamanho_arquivo_em_gb(caminho_arquivo)
            tamanho_formatado = formatar_tamanho_em_gb(tamanho_gb)
            aviso = verificar_tamanho_pst(caminho_arquivo)
            sz = 40

            if tamanho_gb > sz:

                app = QApplication(sys.argv)
                janela = QMainWindow()
                janela.setWindowTitle("Tamanho PST")
                janela.setWindowIcon(QIcon(
                    fr"C:\Users\guilhermemachado\Documents\GitHub\Python-Programs\Size_Archive\alien.ico"))
                janela.setGeometry(100, 100, 400, 200)

                central_widget = QWidget(janela)
                janela.setCentralWidget(central_widget)

                layout = QVBoxLayout()
                label = QLabel()

                if tamanho_gb is not None:
                    if tamanho_gb > sz:
                        label.setText(
                            f"O tamanho do arquivo PST é {tamanho_formatado}")
                        if aviso:
                            label.setText(aviso)
                else:
                    label.setText(
                        f"O arquivo {caminho_arquivo} não foi encontrado")

                if tamanho_gb > sz:
                    label.setAlignment(Qt.AlignCenter)
                    layout.addWidget(label)
                    central_widget.setLayout(layout)

                    janela.show()
                    sys.exit(app.exec_())
            else:
                print(f'caminho do arquivo:  {caminho_arquivo}')
                print('tamanho ok')
        except Exception as e:
            print(f'Parou: {e}')

        sleep(15)


if __name__ == "__main__":
    # Adiciona o script aos serviços de inicialização do Windows
    # add_to_startup()

    main()
