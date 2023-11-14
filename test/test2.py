import paramiko
import pysftp
from ftplib import FTP

# Dodos co servidor FTP origem
host_ftp = '//192.168.0.250/'
port_ftp = 21
user_ftp = 'guilhermemachancoses'
pwd_ftp = 'Gu!@19=#'

# Dodos co servidor SFTP destino
host_sftp = 'euclidesrenato143029.protheus.cloudtotvs.com.br'
port_sftp = 1401
user_sftp = 'ftp_CP4I2U_prod'
pwd_sftp = 'q2fzdbPQCZgTBUCJzJe4Dxn2'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection(host=host_sftp, port=port_sftp, username=user_sftp, password=pwd_sftp,cnopts=cnopts) as sftp:
    
    print ('Conectado...')
    
    diretorio = '1-analistas/bruno/BKP_tabelas'
    
    sftp.cwd(f'/{diretorio}')
    
    directory_structure = sftp.listdir_attr()
    print ('')
    print ('Dirotórios: ')
    print ('')
    
    for attr in directory_structure:
        print (attr.filename, attr)
        