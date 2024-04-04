from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
# Define TF_CPP_MIN_LOG_LEVEL para evitar mensagens de informação do TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from time import sleep
import mysql.connector
from datetime import datetime, timedelta

class zapbot:
    # O local de execução do nosso script
    dir_path = os.getcwd()
    
    # Caminho onde será criada pasta profile
    profile = os.path.join(dir_path, fr"C:\Users\agenda\Documents", "wpp")

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--start-maximized")
        # self.options.add_argument("--headless")
        # Configurando a pasta profile, para mantermos os dados da seção
        self.options.add_argument(r"user-data-dir={}".format(self.profile))
        # Inicializa o webdriver
        self.driver = webdriver.Chrome(options=self.options)
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        # Aguarda alguns segundos para validação manual do QrCode
        self.driver.implicitly_wait(60)

    # abrindo a conversa com o contato:
    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span")))
            # Seleciona a lista de contatos
            self.lista_de_contato = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span").click()
            sleep(1)
            # Seleciona a caixa de pesquisa de conversa
            self.caixa_de_pesquisa = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]/p")
            # Digita o nome ou numero do contato
            self.caixa_de_pesquisa.send_keys(contato)
            sleep(2)
            # Seleciona o contato
            self.contato = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div")
            # Entra na conversa
            self.contato.click()
        except (TimeoutException, NoSuchElementException) as e:
            print("Erro ao abrir conversa:", e)

    # envia mensagens na conversa foi aberta:
    def envia_msg(self, msg):
        """ Envia uma mensagem para a conversa aberta """
        try:
            sleep(5)
            # Seleciona a caixa de mensagem
            self.caixa_de_mensagem = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p")
            # Digita a mensagem
            self.caixa_de_mensagem.send_keys(msg)
            sleep(2)
            # Seleciona botão enviar
            self.botao_enviar = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button")
            # Envia msg
            self.botao_enviar.click()
            sleep(2)
        except NoSuchElementException as e:
            print("Erro ao enviar msg:", e)
    # função para fechar a conexão e finalizar todo processo:
    def finaliza_processo(self):
        """ Fecha a conexão e finaliza o processo """
        self.driver.quit()
        
    def envia_msg_lista_contatos(self, lista_contatos, mensagem):
        try:     
            # Verifica se a lista de contatos está vazia
            if not lista_contatos:
                # Se estiver vazia, define uma lista de contato padrão
                lista_contatos = ['+55 19 98195-5602']
            """ Envia mensagem para uma lista de contatos """
            for contato in lista_contatos:
                self.abre_conversa(contato)
                self.envia_msg(mensagem)
                print(f'mensagem enviada para {contato}')
        except (TimeoutException, NoSuchElementException) as e:
            print("Erro ao enviar msg:", e)
     
    # Estabeleça a conexão com o banco de dados MySQL       
    def conectar_banco_dados(self):
        """Conecta ao banco de dados MySQL e retorna a conexão."""
        try:
            # Conecta ao banco de dados
            connection = mysql.connector.connect(
                host="localhost",
                user="user.mysql",
                password="Fk@35978Gui@19==",
                database="locationlab_db"
            )
            # print("Conexão ao banco de dados MySQL bem-sucedida.")
            return connection
        except mysql.connector.Error as err:
            print("Erro ao conectar ao banco de dados MySQL:", err)
            return None
        
    def consulta_locacao_pendente(self, status):
        # Consulta ao banco de dados MySQL o número de contato dos usuarios referente as locações pendentes
        try:
            # Primeira consulta
            connection = self.conectar_banco_dados()
            cursor = connection.cursor()
            cursor.execute("SELECT timeStamp, locacao_id, users_id FROM `locacao` WHERE status_id = %s AND lc_period_id IS NULL", (status,))
            results = cursor.fetchall()

            locacaoID = []
            verifID = []

            for result in results:
                timestamp_str = str(result[0])
                locacao_id = result[1]
                verif_id = result[2]
                verifID.append(verif_id)
                locacaoID.append(locacao_id)
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                
            for i in verifID:
                cursor.execute("SELECT * FROM `activities` WHERE users_id = %s AND mensagens_id = %s", (i, 45))
                ja_existe = cursor.fetchall()

            if not ja_existe:
                # Caso 'ja_existe' for igual a zero faz:
                data_atual = datetime.now()
                diff = timedelta(days=3)
                contatos = set()  # Use um conjunto para armazenar os contatos únicos
                userIDs = set() # Use um conjunto para armazenar os userID únicos

                for id in locacaoID:
                    soma_data = timestamp + diff                    

                    # Verificar se a data atual é igual ou maior que 3 dias da data do timestamp            
                    if data_atual >= soma_data:

                        # Segunda consulta
                        cursor.execute("""SELECT
                                                u.users_id,
                                                u.contactno
                                        FROM gp_approver as gp
                                        LEFT JOIN users as u
                                        ON u.users_id = gp.users_id
                                        WHERE gp.gp_approver_id = (SELECT gp_approver_id
                                                                    FROM gr_approved as gr 
                                                                    WHERE users_id = (SELECT
                                                                                            u.users_id 
                                                                                        FROM locacao as lc 
                                                                                        INNER JOIN `users` as u ON u.users_id = lc.users_id 
                                                                                        WHERE lc.locacao_id = %s
                                                                                        )
                                                                    )""", (id,))
                        user_results = cursor.fetchall()

                        # Adicionando contatos ao conjunto temporário
                        contatos_temporarios = set()
                        userID_temporarios = set()
                        for user_result in user_results:
                            userID = user_result[0]
                            contato = user_result[1]
                            contatos_temporarios.add(contato)
                            userID_temporarios.add(userID)
                            
                        # Mesclando o conjunto temporário com o conjunto principal de contatos
                        contatos |= contatos_temporarios
                        # Mesclando o conjunto temporário com o conjunto principal de userID
                        userIDs |= userID_temporarios
                try:
                    mensagemID = 45 
                    # Query SQL para inserir dados na tabela activities
                    cursor.execute("""INSERT INTO `activities` (mensagens_id, users_id) VALUES (%s, %s)""", (mensagemID, userID))

                    # Confirma a transação
                    connection.commit()
            
                    print("Dados inseridos com sucesso na tabela activities.")
                except mysql.connector.Error as e:
                    print("Erro ao inserir dados na tabela activities:", e)
                    # Em caso de erro, faça o rollback da transação
                    connection.rollback()

                # Convertendo o conjunto de contatos de volta para lista
                contatos_lista = list(contatos)
                # print("Contatos: ", contatos_lista)
                return contatos_lista

        except mysql.connector.Error as e:
            print("Erro ao conectar ao MySQL:", e)

        finally:
            # Feche o cursor e a conexão com o banco de dados
            if cursor is not None:
                cursor.close()
                # print("Cursor fechado")
            if connection is not None:
                connection.close()
                # print("Conexão com o MySQL fechada")

    
if __name__ == '__main__':
    try:
        # Inicia o objeto zapbot
        bot = zapbot()
        # Define status pendente com valor 1
        status = 1
        # Armazena a lista de contatos retornada pela função
        lista_contatos = bot.consulta_locacao_pendente(status)
        # Verifica se a lista de contatos não está vazia
        if lista_contatos:  
            # Mensagem a ser enviada
            mensagem = "Olá esta é uma mensagem automática do serviço de reserva da Garbuio, você possui solicitações pendente aguardando sua aprovação.\n Acesse em seu navegador o link para aprovar: http://agenda.garbuio.int"
            # Envia mensagem para lista de contatos
            bot.envia_msg_lista_contatos(lista_contatos, mensagem)
        else:
            print("Não há locações pendentes.")
    except KeyboardInterrupt:
        # Finaliza o processo
        print("Usuário parou o precesso.")
        bot.finaliza_processo()
    finally:
        print("Fim.")
        # Finaliza o processo
        bot.finaliza_processo()
    

