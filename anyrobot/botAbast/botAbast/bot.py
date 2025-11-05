"""
Este códdigo foi criado para automatizar os cliques da concistencia de abastecimento

Versão 1.0
Data 17-11-2023
Autor: Guilherme Machancoses

"""

from botcity.core import DesktopBot
from time import sleep


class Bot(DesktopBot):
    def action(self, execution=None):
        
       while True:
            # Verifica se a imagem "click_1" é encontrada                
            if not self.find( "click_1", matching=0.97, waiting_time=10000):
                self.not_found("click_1")            
                
            else:
                self.click()
                print('Alternando 1')
            
            sleep(30)
            
             #Verifica se a imagem "click_1" é encontrada 
            if not self.find( "click_2", matching=0.97, waiting_time=10000):
                self.not_found("click_2")           
            
            else:
                self.click()
                print('Alternando 2')
            
            # Aguarde um tempo antes de iniciar a próxima iteração
            # Isso ajuda a evitar que o loop execute muito rapidamente
            sleep(30)
        

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()

