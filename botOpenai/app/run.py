from Controller.zapbot import ZapBot
from time import sleep
from View.menu import Menu
from Controller.chatBot import Chatbot

class MainApp:
    def __init__(self):
        self.openai = Chatbot()
        self.menu = Menu()
        self.bot = self.menu.bot
        self.bot.abre_conversa("+55 19 98228-0312")
        self.bot.envia_msg("⚡⛑ Olá, sou Guilherme! Para receber ajuda digite: help ⛑⚡")
        self.imagem = self.bot.dir_path + "/Python-Programs/botOpenai/app/image.jpg"
        self.msg = ""
        self.retorno_suporte = ""
        self.imp = ""

    def run(self):
        try:
            while True:
                sleep(2)
                nova_msg = self.bot.ultima_msg()
                if nova_msg != "sair":
                    if nova_msg is not None and nova_msg != self.msg:
                        self.msg = nova_msg
                        if self.msg is not None and self.retorno_suporte == "":
                            
                            if self.msg is not None and self.msg == "help":
                                self.menu.show_menu()
                            elif self.msg is not None and self.msg == "sair":
                                self.menu.sair()
                            elif self.msg is not None and self.msg == "suporte":
                                self.retorno_suporte = self.menu.suporte()
                            elif self.msg is not None and self.msg == "rede":
                                self.menu.rede()
                            elif self.msg is not None and self.msg == "acessos":
                                self.menu.acessos()
                            elif self.msg is not None and self.msg == "totvs":
                                self.menu.totvs()
                            else:
                                self.bot.envia_msg('Desculpe não entendi, por gentileza digite uma opção válida.')
                                
                        elif self.msg is not None and self.retorno_suporte == "1" and self.imp == "":
                            if self.msg == "1":
                                self.imp = self.menu.suporte_impressora()
                            elif self.msg == "2":
                                self.menu.pc_nao_liga()
                        
                        # Envia para openai a mensagem do usuário e depois envia a mensagem de resposta da openai         
                        elif self.msg is not None and self.retorno_suporte == "1" and self.imp == "1":
                            nova_msg = ""
                            while self.msg != "sair" and nova_msg is not None and nova_msg != self.msg:                    
                                msg = self.msg
                                resposta_openai = self.openai.iniciar_conversa(msg)
                                if resposta_openai != "":
                                    # retorna a resposta da openai
                                    self.bot.envia_msg(resposta_openai)
                                    nova_msg = self.bot.ultima_msg()
                                    self.msg = nova_msg
                        else:
                            self.bot.envia_msg('Desculpe não entendi, por gentileza digite uma opção válida.')
                    else:
                        print("Aguardando nova mensagem...")
                else:
                    self.menu.sair()
                    break
                    
        except TimeoutError:
            print("Ocorreu um timeout. Finalizando o programa...")
        except Exception as e:
            print("Ocorreu um erro inesperado:", e)
        finally:
            print("Reiniciando o programa em 2 minutos...")
            sleep(120)  # Espera 2 minutos
            main()
            
def main():
    # Crie uma instância de MainApp e execute o método run
    app = MainApp()
    app.run()

if __name__ == "__main__":
    main()
