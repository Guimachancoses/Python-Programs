from botcity.core import DesktopBot
import pandas as pd
import pyautogui as pg
from time import sleep


class Bot(DesktopBot):

    def action(self, execution=None):

        tabela = pd.read_excel(
            fr'C:\Users\guilhermemachado\Documents\GitHub\BotInsert\db)_users.xlsx')

        # print(tabela)

        # Para cada linha da base de dados faça:
        for linha in tabela.index:

            matricula = str(tabela.loc[linha, 'Matricula'])
            nome = str(tabela.loc[linha, 'Nome']).upper()
            ncard = str(tabela.loc[linha, 'Nº - Cartão'])
            rg = str(tabela.loc[linha, 'RG'])

            if not self.find("novo", matching=0.97, waiting_time=10000):
                self.not_found("novo")
            self.click()

            if not self.find("matricula", matching=0.97, waiting_time=10000):
                self.not_found("matricula")
            self.click()
            pg.write(matricula, interval=0.25)

            if not self.find("name_user", matching=0.97, waiting_time=10000):
                self.not_found("name_user")
            self.click()
            self.paste(nome)

            if not self.find("nc", matching=0.97, waiting_time=10000):
                self.not_found("nc")
            self.click()
            pg.write(ncard, interval=0.25)

            if not self.find("rg", matching=0.97, waiting_time=10000):
                self.not_found("rg")
            self.click()
            pg.write(rg, interval=0.25)

            if not self.find("jor_click", matching=0.97, waiting_time=10000):
                self.not_found("jor_click")
            self.click()

            if not self.find("jor_default", matching=0.97, waiting_time=10000):
                self.not_found("jor_default")
            self.click()
            if not self.find("confir", matching=0.97, waiting_time=10000):
                self.not_found("confir")
            self.click()

            if not self.find("save", matching=0.97, waiting_time=10000):
                self.not_found("save")
            self.click()
            sleep(2)

            if not self.find("sair", matching=0.97, waiting_time=10000):
                self.not_found("sair")
            self.click()
            sleep(2)

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()
