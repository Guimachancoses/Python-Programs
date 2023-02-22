from google_maps import autenticar_api, obter_distancia_entre_pontos
from planilha import ler_planilha, escrever_planilha

def calcular_distancias(df, gmaps):
    """
    Calcula a distância entre cada par de coordenadas na planilha e adiciona uma nova coluna com as distâncias calculadas.
    """
    distancias = []
    for index, row in df.iterrows():
        lat_long = row['LATITUDE_E_LONGITUDE']
        latitude, longitude = lat_long.split(', ')
        distancia = obter_distancia_entre_pontos(gmaps, latitude, longitude)
        distancias.append(distancia)
    df['DISTANCIA'] = distancias
    return df

def main():
    """
    Ponto de entrada do programa.
    """
    caminho_arquivo = 'caminho_para_planilha.xlsx'
    nome_planilha = 'nome_da_planilha'
    chave_api = 'sua_chave_de_API'
    
    gmaps = autenticar_api(chave_api)
    df = ler_planilha(caminho_arquivo, nome_planilha)
    df_com_distancias = calcular_distancias(df, gmaps)
    escrever_planilha(df_com_distancias, caminho_arquivo, nome_planilha)
