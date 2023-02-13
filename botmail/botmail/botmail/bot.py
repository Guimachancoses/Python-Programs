# Automatization for make assign user mail

from cmath import isnan
from time import sleep, time
from botcity.core import DesktopBot
import pyautogui as pg

import pandas as pd

from time import sleep

class Bot(DesktopBot):
    def action(self, execution=None):
        
        # Importar a base de dados       
              
        tabela = pd.read_excel(r'C:\Users\guilhermemachado\Documents\Bkp - USB\Voip\List_User_Assig_2023.xlsx')
        #print(tabela)
        
        # Para cada linha da base de dados faça:
        
        for linha in tabela.index:
            
            self.execute(r"C:\Users\guilhermemachado\Documents\Bkp - USB\Voip\Assinatura.docx")
            sleep(2)
                        
            nome = tabela.loc[linha, 'NomeComp']
            setor = tabela.loc[linha,'Setor']
            telefone = tabela.loc[linha, 'Ramal']
            email = tabela.loc[linha, 'Email']
            link_3cx = tabela.loc[linha, 'Link_3CX']
            
            # Mudar nome do usuário
            
            if not self.find( "Name", matching=0.97, waiting_time=10000):
                self.not_found("Name")
            self.double_click()
            
            if pd.isna(nome):
                self.paste("")
                self.enter()
            
            else: 
            
                self.paste(nome)
                self.enter()
            
            # Mudar Setor
            
            if not self.find( "Sector", matching=0.97, waiting_time=10000):
                self.not_found("Sector")
            self.double_click()
            
            if pd.isna(setor):            
                self.paste('')
                self.enter()
                
            else:
                self.paste(setor)
                self.enter()
            
            # Mudar Ramal
            
            if not self.find( "0000", matching=0.97, waiting_time=10000):
                self.not_found("0000")
            self.double_click()
            
            if pd.isna(telefone):
                self.paste('')
                
            else:
                self.paste(telefone)
            
            # Mudar Email
            
            if not self.find( "change_mailgarb", matching=0.97, waiting_time=10000):
                self.not_found("change_mailgarb")                           
            self.click()
            
            if not self.find( "Inserir", matching=0.97, waiting_time=10000):
                self.not_found("Inserir")
            self.click()
            
            if not self.find( "Link", matching=0.97, waiting_time=10000):
                self.not_found("Link")
            self.click()
            
            if not self.find( "Link2", matching=0.97, waiting_time=10000):
                self.not_found("Link2")
            self.click()
            
            if not self.find( "cgmail", matching=0.97, waiting_time=10000):
                self.not_found("cgmail")
            self.click()                      
            self.control_a()
            self.delete()
            
            if pd.isna(email):
                self.paste("suporte@garbuio.com.br")
                sleep(0.1)
                
            else:
                self.paste(email)
                sleep(0.1)
            
            if not self.find( "mailto", matching=0.97, waiting_time=10000):
                self.not_found("mailto")
            self.click()            
            self.control_a()
            self.delete()
            
            if pd.isna(email):
                self.paste("suporte@garbuio.com.br")
                sleep(0.1)
                
            else:
                self.paste(email)
                sleep(0.1)
           
            if not self.find( "ckok", matching=0.97, waiting_time=10000):
                self.not_found("ckok")
            self.click()
            sleep(0.1)            
            
            # Mudar link 3CX
            
            if not self.find( "Comigo", matching=0.97, waiting_time=10000):
                self.not_found("Comigo")
            self.click()
            
            if not self.find( "Link", matching=0.97, waiting_time=10000):
                self.not_found("Link")
            self.click()
            
            if not self.find( "Link2", matching=0.97, waiting_time=10000):
                self.not_found("Link2")
            self.click()            
            
            if not self.find( "change_link", matching=0.97, waiting_time=10000):
                self.not_found("change_link")
            self.click()
            self.control_a()
            self.delete()
            
            if pd.isna(link_3cx):
                self.paste("https://garbuio.my3cx.com.br/suporteti")
            
            else:
                self.paste(link_3cx)
            
            if not self.find( "ckok2", matching=0.97, waiting_time=10000):
                self.not_found("ckok2")
            self.click()                           
            
            # Salvar assinatura com nome de usuário
              
            pg.press('f12')      
            
            if not self.find( "nome_user", matching=0.97, waiting_time=10000):
                self.not_found("nome_user")
            self.paste(nome)
            self.enter()
            self.alt_f4()           
            
                               
    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()




##