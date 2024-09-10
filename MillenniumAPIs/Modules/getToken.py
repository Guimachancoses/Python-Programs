import requests

def getToken():
    # URL da API
    url = "https://api3-ng.tracknow.com/auth/login"

    # Corpo da requisição
    payload = {
        "userName": "BI_GARBUIO",
        "password": "3dTJJf@e"
    }

    try:
        # Realiza a requisição POST
        response = requests.post(url, json=payload)

        # Verifica se a requisição foi bem-sucedida (código de status 200)
        response.raise_for_status()

        # Converte a resposta JSON em um dicionário Python
        data = response.json()

        # Obtém o token da resposta e retorna
        token = data.get("data", {}).get("token")
        return token

    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição: {err}")

    return None

# Exemplo de uso da função getToken()
# token = getToken()
# if token:
#     print("Token:", token)
# else:
#     print("Falha ao obter o token.")
