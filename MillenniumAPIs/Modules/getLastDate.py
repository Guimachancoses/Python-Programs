import pyodbc
from Modules.connectSQL import connect_to_database
from datetime import datetime

def get_last_event_timestamp(view, connection):
    cursor = connection.cursor()
    
    try:
        # Executa a consulta para obter a última data
        query = view
        cursor.execute(query)
        
        # Recupera o resultado
        result = cursor.fetchone()
        if result and result[0]:
            # Converte a string retornada para um objeto datetime
            last_event_timestamp_str = result[0]
            try:
                # Ajuste o formato de entrada se necessário, exemplo: '2024-08-01 18:07:34-03'
                last_event_timestamp = datetime.fromisoformat(last_event_timestamp_str.replace("Z", "+00:00"))
                
                # Formata a data no formato desejado
                # formatted_timestamp = last_event_timestamp.strftime("%Y-%m-%d+%H:%M:%S")
                print("------------------------------------------------------")
                print(f"Última data do evento retornada: {last_event_timestamp}")
                print("------------------------------------------------------\n")
                return last_event_timestamp
            except ValueError as e:
                print(f"Erro ao converter a data: {e}")
                return None
        else:
            last_event_timestamp = "2024-08-01 00:00:00-03"
            event_time = datetime.fromisoformat(last_event_timestamp.replace("Z", "+00:00"))
            return event_time
    
    except pyodbc.Error as e:
        print(f"Erro ao executar a consulta: {e}")
        return None
    
    finally:
        cursor.close()

# Exemplo de uso da função get_last_event_timestamp
# if __name__ == "__main__":
#     # Estabelece a conexão com o banco de dados
#     connection = connect_to_database()
    
#     if connection:
#         # Obtém a última data do evento e a formata
#         get_last_event_timestamp(connection)
#         # Fecha a conexão com o banco de dados
#         connection.close()
