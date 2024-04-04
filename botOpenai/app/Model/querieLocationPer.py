from Model.database import Database

class Queries:
    @staticmethod
    def consul_loc_pend_periodo(IDlocation):
        # Consulta ao banco de dados MySQL o número de contato dos usuarios referente as locações pendentes
        try:
            # Primeira consulta
            connection = Database.conectar_banco_dados()
            cursor = connection.cursor()
            cursor.execute("""SELECT
                                    u.contactno
                            FROM gp_approver as gp
                            LEFT JOIN users as u
                            ON u.users_id = gp.users_id
                            WHERE gp.gp_approver_id = (SELECT gp_approver_id
                                                        FROM gr_approved as gr 
                                                        WHERE users_id = (SELECT
                                                                                u.users_id 
                                                                            FROM lc_period as lc 
                                                                            INNER JOIN `users` as u ON u.users_id = lc.users_id 
                                                                            WHERE lc.lc_period_id = %s
                                                                            )
                                                        )""", (IDlocation,))
            results = cursor.fetchall()

            contatos = []
            
            if results:
                contato = results[0]
                contatos.append(contato)
            
            print (" Contatos: %s" % contatos)                  

            return contatos

        except connection.connector.Error as e:
            print("Erro ao conectar ao MySQL:", e)

        finally:
            # Feche o cursor e a conexão com o banco de dados
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
