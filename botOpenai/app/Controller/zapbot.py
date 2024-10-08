from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import os

class ZapBot:
    # O local de execução do nosso script
    dir_path = os.getcwd()
    
    # Caminho onde será criada pasta profile
    profile = os.path.join(dir_path, fr"C:\Users\SAMSUMG\OneDrive\Documentos", "wpp")

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
        
    # Inicia whatapp e filtra por conversas não lidas:
    def iniciar_whats_filtrando(self, mensagem):
        try:
            WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/button')))
            # Seleciona a lista de contatos
            self.lista_de_contato = self.driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/button').click()
            sleep(1)
            
            # Encontra a notificação de mensagem não lida
            WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, '2H6nH')))
                        
            # Encontre todos os elementos com a classe "2H6nH"
            elementos = self.driver.find_elements(By.CLASS_NAME, "2H6nH")

            # Clique no primeiro elemento
            elementos[0].click()
            
            if elementos:
                self.envia_msg(mensagem)
            else:
                return None
        except (TimeoutException, NoSuchElementException) as e:
            print("Erro ao abrir conversa:", e)


    # abrindo a conversa com o contato:
    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span")))
            # Seleciona a lista de contatos
            self.lista_de_contato = self.driver.find_element(By.XPATH, "//*[@id='app']/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span").click()
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
            self.botao_enviar = self.driver.find_element(By.CSS_SELECTOR, '[data-tab="11"]')
            sleep(1)
            # Envia msg
            self.botao_enviar.click()
            sleep(2)
        except NoSuchElementException as e:
            print("Erro ao enviar msg:", e)
            
    # função para fechar a conexão e finalizar todo processo:
    def finaliza_processo(self):
        """ Fecha a conexão e finaliza o processo """
        self.driver.quit()
        
    # envia mensagens ao usuário    
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

    # envia midia
    def envia_media(self, fileToSend):
        """ Envia media """
        try:
            # Clica no botão adicionar
            self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
            # Seleciona input
            attach = self.driver.find_element_by_css_selector("input[type='file']")
            # Adiciona arquivo
            attach.send_keys(fileToSend)
            sleep(3)
            # Seleciona botão enviar
            send = self.driver.find_element_by_xpath("//div[contains(@class, 'yavlE')]")
            # Clica no botão enviar
            send.click()
        except Exception as e:
            print("Erro ao enviar media", e)
    
    # Verifica qual a ultima mensagem recebida pelo usuário:        
    def ultima_msg(self):

        try:
            # Encontre todos os elementos com a classe "message-in"
            elementos = self.driver.find_elements(By.CLASS_NAME, "message-in")
            
            # Inicialize uma lista vazia para armazenar os textos das mensagens
            lista_resposta = []
            lista_horas = []

            # Itere sobre os elementos encontrados e adicione os textos à lista_resposta
            for elemento in elementos:
                texto = elemento.text.strip()
                if texto:  # Verifica se o texto não está vazio
                    msg = str(texto[0:-6])
                    hora = str(texto[-5:])
                    lista_resposta.append(msg)
                    lista_horas.append(hora)

            # Verifique se há pelo menos uma mensagem antes de acessar a última
            if lista_resposta:
                ultimo_valor = lista_resposta[-1]
                ultima_hora = lista_horas[-1]
                
                # Obtém a hora atual
                hora_ult_msg_env = self.hora_ultima_msg_enviada()
                
                if ultima_hora < hora_ult_msg_env:
                    return None
                else:
                    return ultimo_valor
            else:
                print("Nenhuma mensagem encontrada")
                return None

        except Exception as e:
            print("Erro ao ler msg, tentando novamente!")
            
    # Verifica qual a hora que foi enviada uma mensagem ao usuário:        
    def hora_ultima_msg_enviada(self):

        try:
            # Encontre todos os elementos com a classe "message-in"
            elementos = self.driver.find_elements(By.CLASS_NAME, "message-out")
            
            # Inicialize uma lista vazia para armazenar os textos das mensagens
            lista_horas = []

            # Itere sobre os elementos encontrados e adicione os textos à lista_resposta
            for elemento in elementos:
                texto = elemento.text.strip()  # Remova espaços em branco extras
                if texto:  # Verifica se o texto não está vazio
                    hora = str(texto[-5:])
                    lista_horas.append(hora)

            # Verifique se há pelo menos uma mensagem antes de acessar a última
            if lista_horas:
                ultima_hora = lista_horas[-1]                
                return ultima_hora
            else:
                print("Nenhuma hora encontrada")
                return None

        except Exception as e:
            print("Erro ao ler msg, tentando novamente!")