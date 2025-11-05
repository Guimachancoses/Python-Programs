import pyodbc

def connect_to_database():
    # Configuração da conexão
    server = 'Agenda'  # Nome do servidor
    database = 'DBGarmill'  # Substitua pelo nome do seu banco de dados
    username = 'GarmillAdmin'  # Nome de logon
    password = 'G@rbu!o23ERG'  # Senha

    # Conexão com o banco de dados usando pyodbc
    try:
        # Definição da string de conexão
        connection_string = (
            f'DRIVER={{SQL Server}};'  # O driver ODBC para SQL Server
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
            f'Encrypt=no;'  # Criptografia opcional
        )
        
        # Estabelece a conexão
        connection = pyodbc.connect(connection_string)

        print("Conexão bem-sucedida!")

        return connection

    except pyodbc.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# # Exemplo de uso da função connect_to_database
# connection = connect_to_database()

# if connection:
#     # Você pode executar consultas SQL usando a conexão
#     cursor = connection.cursor()
#     cursor.execute("SELECT @@version;")  # Exemplo de consulta SQL
#     row = cursor.fetchone()
#     while row:
#         print(row)
#         row = cursor.fetchone()

#     # Fechar a conexão quando terminar
#     connection.close()
# else:
#     print("Não foi possível estabelecer a conexão.")
