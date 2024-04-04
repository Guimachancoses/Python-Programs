import openai

class Chatbot:
    def __init__(self):
        self.key = 'chave_api'
        self.api_key = self.key
        openai.api_key = self.key

    def enviar_mensagem(self, mensagem, lista_mensagens=[]):
        lista_mensagens.append(
            {"role": "user", "content": mensagem}
        )
        
        resposta = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = lista_mensagens,
        )
        
        return resposta.choices[0].message.content

    def iniciar_conversa(self, mensagem):
        listaMensagens = [
            {"role": "system", "content": "You are a helpful assistant designed to answer simple questions in no more than 10 words about printer problems."},
        ]            
        resposta = self.enviar_mensagem(mensagem, listaMensagens)
        listaMensagens.append(resposta)
        
        if len(resposta.split()) > 10:
            return "Aguarde,um dos nossos técnicos irá lhe atender."
        else:
            return resposta

# Exemplo de uso:
# chave_api = "suaaa_chave_api"
# meu_chatbot = Chatbot(chave_api)
# meu_chatbot.iniciar_conversa()
