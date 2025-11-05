import googlemaps

def autenticar_api(chave_api):
    """
    Autentica na API do Google Maps usando a chave da API fornecida.
    Retorna um objeto Client que será utilizado para fazer as requisições.
    """
    try:
        gmaps = googlemaps.Client(key=chave_api)
    except googlemaps.exceptions.ApiError as e:
        print(f"Erro ao autenticar na API do Google Maps: {e}")
        return None
    else:
        return gmaps

def obter_distancia_entre_pontos(gmaps, latitude, longitude, latitude2, longitude2):
    """
    Chama a API do Google Maps para obter a distância entre dois pontos.
    Retorna a distância em uma string.
    """
    try:
        directions_result = gmaps.directions(
            "place1={0},{1}".format(latitude, longitude), 
            "place2={0},{1}".format(latitude2, longitude2), 
            mode="driving"
        )
        distance = directions_result[0]['legs'][0]['distance']['text']
    except (googlemaps.exceptions.ApiError, IndexError) as e:
        print(f"Erro ao obter a distância entre os pontos ({latitude}, {longitude}): {e}")
        return None
    else:
        return distance

    
    
