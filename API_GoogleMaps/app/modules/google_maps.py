import googlemaps

def autenticar_api(chave_api):
    """
    Autentica na API do Google Maps usando a chave da API fornecida.
    Retorna um objeto Client que será utilizado para fazer as requisições.
    """
    gmaps = googlemaps.Client(key=chave_api)
    return gmaps

def obter_distancia_entre_pontos(gmaps, latitude, longitude):
    """
    Chama a API do Google Maps para obter a distância entre dois pontos.
    Retorna a distância em uma string.
    """
    directions_result = gmaps.directions("place1={0},{1}".format(latitude, longitude), "place2={0},{1}".format(latitude, longitude), mode="driving")
    distance = directions_result[0]['legs'][0]['distance']['text']
    return distance
