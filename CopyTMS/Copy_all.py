from shutil import copyfile
from time import sleep
import os
import traceback
import pysftp
from datetime import datetime
from tqdm import tqdm
from telegram import Bot
import asyncio

# Token do seu bot no Telegram
TELEGRAM_BOT_TOKEN = '6518320842:AAGKHeujfkguXWC0csr_SltNsgopPxm7vNw'

# ID do chat ou número para onde a mensagem será enviada
TELEGRAM_CHAT_ID = '6600221215'

# Dados do servidor SFTP destino
host_sftp = 'euclidesrenato143029.protheus.cloudtotvs.com.br'
port_sftp = 1401
user_sftp = 'ftp_CP4I2U_prod'
pwd_sftp = 'q2fzdbPQCZgTBUCJzJe4Dxn2'

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# Função copiar arquivo de origem para destino
def copy_file():
    # Conectar ao destino (SFTP)
    with pysftp.Connection(host=host_sftp, port=port_sftp, username=user_sftp, password=pwd_sftp, cnopts=cnopts) as sftp:
        print('Conectado...')

        # Diretório origem dos arquivos que serão copiados:
        orig_dir = fr"X:"

        # Primeiro diretório destino para onde os arquivos serão copiados
        dest_dir = '/xmlnfe/new'

        # Segundo diretório destino para onde os arquivos serão copiados
        dest_dir_seg = 'J:\Guilherme\ImportadosTMS'

        # Mudar para o diretório destino no servidor SFTP
        sftp.cwd('/')

        # Criar o diretório de destino se não existir
        sftp.makedirs(dest_dir)

        # Mudar para o diretório destino no servidor SFTP
        sftp.cwd(dest_dir)

        # Listar os arquivos de origem
        listdir = os.listdir(f'{orig_dir}/')
        
        # Verificar se a lista está vazia
        if not listdir:
            print('Nenhum arquivo para copiar. Encerrando o script.')
            return

        # Obter a data e hora atual para criar o nome da nova pasta
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nova_pasta = f'importado_{timestamp}'

        # Caminho completo para a nova pasta dentro de dest_dir_seg
        dest_dir_nova_pasta = os.path.join(dest_dir_seg, nova_pasta)

        # Criar a nova pasta
        os.makedirs(dest_dir_nova_pasta)

        # Iterar sobre cada arquivo da lista de origem com uma barra de progresso
        for arquivo in tqdm(listdir, desc="Copiando arquivos", unit="arquivo"):
            origem = os.path.join(orig_dir, arquivo)
            destino_sftp = f'{dest_dir}/{arquivo}'  # Caminho no servidor remoto
            destino_local = os.path.join(dest_dir_nova_pasta, arquivo)  # Caminho local bkp
            
            # verifica se o arquivo já existe no local destino SFTP se sim subistitui
            if sftp.exists(destino_sftp):
                sftp.remove(destino_sftp)
            # Se todas as variáveis possuírem retorno, cole no primeiro destino
            sftp.put(origem, destino_sftp)

            # verifica se o arquivo já existe no local destino BKP se sim subistitui
            if os.path.exists(destino_local):
                os.remove(destino_local)
            # Se todas as variáveis possuírem retorno, cole no segundo destino
            copyfile(origem, destino_local)

            # Limpa o diretório de origem após copiar para os dois destinos
            os.remove(origem)

    print('Processo concluído!')

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


def main():
    max_attempts = 10
    wait_time = 300  # segundos
    attempt = 1

    try:
        while attempt <= max_attempts:
            try:
                copy_file()
                print("Arquivo copiado com sucesso!")
                asyncio.run(send_telegram_message("Processo concluído com sucesso!"))
                break

            except PermissionError as e:
                print(f"Erro ao copiar o arquivo: {e}")
                asyncio.run(send_telegram_message(f"Erro ao copiar o arquivo: {e}"))

            except Exception as e:
                print(f'Error: {e}')
                traceback.print_exc()
                asyncio.run(send_telegram_message(f'Erro no processo: {e}'))

            if attempt == max_attempts:
                print("Não foi possível substituir o arquivo pois ele está sendo usado por outro processo.")
                asyncio.run(send_telegram_message("Não foi possível substituir o arquivo pois ele está sendo usado por outro processo."))
                break

            else:
                print(f"Tentando novamente em {wait_time} segundos...")
                asyncio.run(send_telegram_message(f"Tentando novamente em {wait_time} segundos..."))
                sleep(wait_time)
                attempt += 1

    except Exception as e:
        print(f'Erro geral: {e}')
        traceback.print_exc()
        asyncio.run(send_telegram_message(f'Erro geral: {e}'))

if __name__ == '__main__':
    main()
