from Controller.zapbot import ZapBot

class Menu:
    def __init__(self):
        self.bot = ZapBot()

    # Chama as opções do menu:
    def show_menu(self):
        self.bot.envia_msg("""GuiBot: Esse é um texto com os comandos válidos digite:
                        🛠️ - suporte (para saber mais)
                        🌐 - rede (para saber mais)
                        🔑 - acessos (para saber mais)
                        💻 - totvs (para saber mais)
                        ❌ - sair (para encerrar) \n Digite uma das opções.""")

    # Caso a oção for suporte mostra:
    def suporte(self):
        suporte = "1"
        self.bot.envia_msg("""GuiBot: Esse é um texto com os comandos válidos:
                        🖨️ 1 - (problema com a impressora)
                        🖥️ 2 - (computador não liga)
                        ◀️ - help (voltar ao menu)
                        ❌ - sair (para encerrar) \n Digite uma das opções.""")
        return suporte

    # Caso escolha em suporte for 1:
    def suporte_impressora(self):
        imp = "1"
        self.bot.envia_msg("Entendo, você está com problema na impressora. \n Qual o problema que você está enfrentando?")
        return imp

    # Caso escolha em suporte for 2:
    def pc_nao_liga(self):
        pcOff = "1"
        self.bot.envia_msg("Entendo, vou direcioná-lo para um de nossos técnicos.")
        return pcOff

    # Caso a oção for rede mostra:
    def rede(self):
        rede = "1"
        self.bot.envia_msg("""GuiBot: Esse é um texto com os comandos válidos:
                        🌐 1 - (sem internet)
                        🛜 2 - (vpn não funciona)
                        💻 3 - (site não funciona)
                        ◀️ - help (voltar ao menu)
                        ❌ - sair (para encerrar) \n Digite uma das opções.""")
        return rede

    # Caso a oção for acessos mostra:
    def acessos(self):
        acesssos = "1"
        self.bot.envia_msg("""GuiBot: Esse é um texto com os comandos válidos:
                        🔑 1 - (troca de senha)
                        🔓 2 - (desbloqueio ou liberação)
                        ◀️ - help (voltar ao menu)
                        ❌ - sair (para encerrar)\n Digite uma das opções.""")
        return acesssos

    # Caso a oção for Totvs mostra:
    def totvs(self):
        acesssos = "1"
        self.bot.envia_msg("""GuiBot: Esse é um texto com os comandos válidos:
                        🔒 1 - (usuário preso)
                        ❗ 2 - (sistema travado)
                        🚫 3 - (erro na rotina)
                        ◀️ - help (voltar ao menu)
                        ❌ - sair (para encerrar)\n Digite uma das opções.""")
        return acesssos

    # Caso a oção for sair mostra:
    def sair(self):
        self.bot.envia_msg("Obrigado até a próxima!")
        return False
