from modules.google_maps import autenticar_api, obter_distancia_entre_pontos
from modules.planilha import ler_planilha, escrever_planilha

def calcular_distancias(df, gmaps):
    """
    Calcula a distância entre cada par de coordenadas na planilha e adiciona uma nova coluna com as distâncias calculadas.
    """
    distancias = []
    for index, row in df.iterrows():
        lat_long_dest = row['LATITUDE_E_LONGITUDE']
        latitude, longitude = lat_long_dest.split(', ')
        lat_long_orig = row['ORIGEM']
        latitude2, longitude2 = lat_long_orig.split(', ')
        distancia = obter_distancia_entre_pontos(gmaps, latitude, longitude, latitude2, longitude2)
        if distancias is not None:
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
    try:
        gmaps = autenticar_api(chave_api)
        if not gmaps:
            return None
        try:
            df = ler_planilha(caminho_arquivo, nome_planilha)
        except FileNotFoundError as e:
            print(f"Arquivo ou planilha não encontrada: {e}")
        # return None
        df_com_distancias = calcular_distancias(df, gmaps)
        if df_com_distancias is not None:
            escrever_planilha(df_com_distancias, caminho_arquivo, nome_planilha)
    except Exception as e:
        print('Ocorreu um erro:', e)
    
    