import mysql.connector

class Database:
    @staticmethod
    def conectar_banco_dados():
        """Conecta ao banco de dados MySQL e retorna a conexão."""
        try:
            # Conecta ao banco de dados
            connection = mysql.connector.connect(
                host="localhost",
                user="user.mysql",
                password="Fk@35978Gui@19==",
                database="locationlab_db"
            )
            return connection
        except mysql.connector.Error as err:
            print("Erro ao conectar ao banco de dados MySQL:", err)
            return None
