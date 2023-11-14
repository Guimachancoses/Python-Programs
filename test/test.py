from ftplib import FTP
import paramiko
from io import BytesIO

def transferir_sftp(origem_servidor, destino_servidor, origem_porta, destino_porta, origem_dir, destino_dir, origem_usuario, destino_usuario, origem_senha, destino_senha):
    # Conectar ao servidor de origem (FTP)
    ftp_origem = FTP()
    ftp_origem.connect(origem_servidor, origem_porta)
    ftp_origem.login(user=origem_usuario, passwd=origem_senha)

    # Conectar ao servidor de destino (SFTP)
    destino_ssh = paramiko.SSHClient()
    destino_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    destino_ssh.connect(destino_servidor, destino_porta, username=destino_usuario, password=destino_senha)
    destino_sftp = destino_ssh.open_sftp()

    # Mudar para o diretório de origem (FTP)
    ftp_origem.cwd(origem_dir)

    # Listar arquivos no diretório de origem (FTP)
    arquivos = ftp_origem.nlst()

    # Transferir arquivos do servidor de origem (FTP) para o servidor de destino (SFTP)
    for arquivo in arquivos:
        temp_file = BytesIO()
        ftp_origem.retrbinary(f"RETR {arquivo}", temp_file.write)
        temp_file.seek(0)
        destino_sftp.putfo(temp_file, f"{destino_dir}/{arquivo}")

    # Fechar as conexões FTP e SFTP
    ftp_origem.quit()
    destino_sftp.close()
    destino_ssh.close()

# Exemplo de uso
transferir_sftp('192.168.0.250', 'euclidesrenato143029.protheus.cloudtotvs.com.br', 21, 1401, '/X:/', '/xmlnfe/new', 'guilhermemachancoses', 'ftp_CP4I2U_prod', 'Gu!@19=#', 'q2fzdbPQCZgTBUCJzJe4Dxn2')
