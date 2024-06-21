"""
Este código foi criado para automatizar os cliques do monitor de hodômetro Protheus

Versão 1.0
Data 24-04-2024
Autor: Guilherme Machancoses

"""

from botcity.core import DesktopBot
from time import sleep


class Bot(DesktopBot):
    def action(self, execution=None):
        
        while True:
            
            try:

                # Com o Protheus aberto, e a rotina do monitor de hodômetro faça:              
                # Alterne as telas do protheus:
                # Tela 1:
                if not self.find( "alterna1", matching=0.97, waiting_time=10000):
                    print("Aguardando o 'Tela Menu'...")
                    pass
                else:
                    self.click()
                    sleep(1)

                # Tela 2:
                if not self.find( "alterna2", matching=0.97, waiting_time=10000):
                    print("Aguardando o 'Tela monitor de Hôdometro'...")
                    pass
                else:
                    self.click()
                    sleep(1)
                    
                # Clica na tela do Protheus para começar:
                if not self.find( "click_recebidos", matching=0.97, waiting_time=10000):
                    print("Aguardando o 'clique fora'...")
                    pass
                else:
                    self.double_click()
                    
                # Encontre o botão de outras ações: 
                if not (self.find( "outras_acors2", matching=0.97, waiting_time=10000) or self.find( "outras_acoes", matching=0.97, waiting_time=10000) or self.find( "outras_acoes1", matching=0.97, waiting_time=10000)):               
                    print("Aguardando a presença da imagem 'Outras ações'...")
                    pass
                else:    
                    self.click()
                    print ('Outras Ações - OK')
                    
                # Encontre o botão de efetivação em lote:
                if not self.find( "efetiv_lote", matching=0.97, waiting_time=10000):
                    print("Aguardando a presença da imagem 'Efetivação em lote'...")
                    pass                
                else:
                    self.click()
                    print ('Efetivação em Lote - OK')
                
                # Encontra o botão de 'Sim', para confirmar efetivação:                    
                if not (self.find( "confirm_efetiv", matching=0.97, waiting_time=10000) or self.find( "click_sim1", matching=0.97, waiting_time=10000) or self.find( "click_sim2", matching=0.97, waiting_time=10000)):
                    print("Aguardando a presença da imagem 'Confirmar efetivação'...")
                    pass
                else:
                    self.click()
                    print ('Sim, confirma efetivação - OK')
                
                # Aguarda o processo da efetivação, ao terminar clica em 'Fechar':                                    
                if not (self.find( "click_fechar", matching=0.97, waiting_time=10000) or self.find( "click_fechar2", matching=0.97, waiting_time=10000) or self.find( "click_fechar3", matching=0.97, waiting_time=10000)):
                    print("Aguardando a presença da imagem 'Clicar em fechar'...")
                    pass
                else:
                    self.click()
                    print ('Fechar - OK')                              
                  
                  
            except Exception as e:
                print(f"Error: {e}")
                self.action()
 
    def not_found(self, label):
        print(f"Element not found: {label}")

if __name__ == '__main__':
    Bot.main()
