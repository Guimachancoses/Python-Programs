import time
from Modules.getToken import getToken
import requests

# Função para fazer a solicitação ao endpoint com os parâmetros datefrom e dateto
def fetchEventReport(endpoint):
    # Obter o token usando a função getToken
    token = getToken()
    if not token:
        print("Falha ao obter o token.")
        return None

    # Configurar a URL do endpoint com os parâmetros datefrom e dateto
    url = endpoint

    # Exibir a URL que será usada na requisição
    # print(f"URL da requisição: {url}")

    # Configurar os headers da requisição com o token
    headers = {
        "Authorization": f"Bearer {token}"
    }

    retries = 3  # Número de tentativas
    retry_delay = 2  # Tempo de espera entre as tentativas em segundos

    for attempt in range(retries):
        try:
            # Fazer a requisição GET ao endpoint
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Converter a resposta JSON em um dicionário Python
            data = response.json()
            return data

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 500:
                print(f"Tentativa {attempt + 1} de {retries} falhou com erro 500. Tentando novamente em {retry_delay} segundos...")
                time.sleep(retry_delay)
            else:
                print(f"Erro HTTP não recuperável: {http_err}")
                break  # Se for um erro diferente de 500, sai do loop

        except requests.exceptions.RequestException as err:
            print(f"Erro na requisição: {err}")
            break  # Para outros tipos de erro, sai do loop imediatamente

    print("Falha após múltiplas tentativas.")
     # Exibir a URL que será usada na requisição
    print(f"URL da requisição: {url}")
    return None



# Exemplo de uso da função fetchEventReport
# datefrom = "2024-05-16+00:00"
# dateto = "2024-05-16+23:59"
# event_report = fetchEventReport(datefrom, dateto)

# if event_report:
#     print("Dados do Relatório de Eventos:", event_report)
# else:
#     print("Falha ao obter os dados do relatório de eventos.")


