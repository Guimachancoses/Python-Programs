import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession, GenerationConfig, FunctionDeclaration, Tool
from googleSearchBot import PesquisaGoogle

# TODO(developer): Update and un-comment below lines

class Chatbot:
    def __init__(self):
        self.project_id = "geminibot-419111"
        self.location = "us-central1"
        vertexai.init(project=self.project_id, location=self.location)
        self.model = GenerativeModel("gemini-1.0-pro")
        # self.search =  PesquisaGoogle()
        self.chat = self.model.start_chat()
        self.lista_mensagens=[]

    def get_chat_response(self, chat: ChatSession, prompt: str, lista_mensagens=[]):
        lista_mensagens.append(
            {"role": prompt}
        )
        
        config = GenerationConfig(
            max_output_tokens=525,
            temperature=0.7,
        )
                   
        resposta = chat.send_message(
            prompt,
            generation_config=config # Configuração de geração
        )
        
        # msg = prompt
        
        # links = self.search.enviar_pergunta(msg)
                
        return resposta.text

    def iniciar_conversa(self, mensagem):
        # Adiciona "Resuma em 20 palavras:" à mensagem recebida
        mensagem = "Relacione a minha dúvida ao assuntos do 'Protheus - Totvs' e envie uma resposta resumida a 100 palavras sobre a minha duvida, e caso a minha pergunta não for relacionada a 'Totvs - Protheus', envie 'Desculpe, não tenho essa informação.': " + mensagem + " Protheus" 
        resposta = self.get_chat_response(self.chat, mensagem)
            
        if len(resposta.split()) > 370:
            return "Sua pergunta foi muito complexa para ser respondida automaticamente. Aguarde, um de nossos técnicos irá atendê-lo em breve."
        else:
            return resposta
        
# Exemplo de uso:
meu_chatbot = Chatbot()
search =  PesquisaGoogle()
while True:
    texto = input('Digite sua dúvida ou "Encerrar", se quiser parar: ').strip()
    if (texto.lower() != "encerrar"):
        resposta = meu_chatbot.iniciar_conversa(texto)
        links = search.enviar_pergunta(texto)
        print(resposta, "\n", links)
    else:
        print("Obrigado até a próxima!")
        break
