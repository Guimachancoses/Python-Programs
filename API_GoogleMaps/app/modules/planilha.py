import pandas as pd

def ler_planilha(caminho_arquivo, nome_planilha):
    """
    Lê a planilha de Excel contendo as coordenadas.
    Retorna um objeto DataFrame com as coordenadas.
    """
    df = pd.read_excel(caminho_arquivo, sheet_name=nome_planilha)
    return df

def escrever_planilha(df, caminho_arquivo, nome_planilha):
    """
    Escreve as mudanças realizadas na planilha em um arquivo de Excel.
    """
    try:
        writer = pd.ExcelWriter(caminho_arquivo, engine='openpyxl') 
        writer.book = pd.read_excel(caminho_arquivo)
        df.to_excel(writer, sheet_name=nome_planilha, index=False)
        writer.save()
    except Exception as e:
        print(f"Erro ao salvar a planilha: {e}")
