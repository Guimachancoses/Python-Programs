import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession, GenerationConfig, FunctionDeclaration, Tool

# TODO(developer): Update and un-comment below lines

class Chatbot:
    def __init__(self):
        self.project_id = "geminibot-419111"
        self.location = "us-central1"
        vertexai.init(project=self.project_id, location=self.location)
        self.model = GenerativeModel("gemini-1.0-pro")
        self.chat = self.model.start_chat()
        self.lista_mensagens=[]

    def get_chat_response(self, chat: ChatSession, prompt: str, lista_mensagens=[]):
        lista_mensagens.append(
            {"role": prompt}
        )
        
        config = GenerationConfig(max_output_tokens=100)
                   
        resposta = chat.send_message(
            prompt,
            generation_config=config # Configuração de geração
        )
        return resposta.text

    def iniciar_conversa(self, mensagem, lista_mensagens):
        # Adiciona "Resuma em 20 palavras:" à mensagem recebida
        mensagem = "Resuma em 40 palavras: " + mensagem
        resposta = self.get_chat_response(self.chat, mensagem, lista_mensagens)
        if len(resposta.split()) > 45:
            return "Aguarde, um de nossos técnicos irá atendê-lo em breve."
        else:
            return resposta

# Exemplo de uso:
while True:
    meu_chatbot = Chatbot()
    texto = input('Digite sua dúvida ou "Encerrar", se quiser parar: ')
    lista_mensagens = []
    if texto != "Encerrar":
        resposta = meu_chatbot.iniciar_conversa(texto, lista_mensagens)
        lista_mensagens.append(resposta)
        print(resposta)
    else:
        print("Obrigado até a próxima!")
        break

