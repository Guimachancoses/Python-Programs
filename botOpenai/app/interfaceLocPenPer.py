from Controller.zapbot import ZapBot
from Model.querieLocationPer import Queries
import json
import sys

if __name__ == '__main__':
    try:
        # Recebe o argumento JSON da linha de comando
        IDlocation_json = sys.argv[1]
        print(" Argumento JSON recebido:", IDlocation_json)

        # Decodifica o argumento JSON
        IDlocation = json.loads(IDlocation_json)
        
        # Acessa o valor associado à chave 'IDlocation'
        IDlocation_value = IDlocation.get('IDlocation')
        print(f"IDlocation valor: {IDlocation_value}")
        
        # Verifica se IDlocation_value é maior que 1
        if IDlocation_value is not None and IDlocation_value > 1:
            print(f" IDlocation valor: {IDlocation_value}")
        else:
            print("Não tive a capacidade de decodificar direito pois não sei pegar apenas o valor de '{'IDlocation:77'}'")
        
        # Inicia o objeto zapbot
        bot = ZapBot()

        # Verifica se há argumentos de linha de comando
        if len(sys.argv) > 1:
                    
            # Armazena a lista de contatos retornada pela função
            lista_contatos = Queries.consul_loc_pend_periodo(IDlocation_value)
            # Verifica se a lista de contatos não está vazia
            if lista_contatos:  
                # Mensagem a ser enviada
                mensagem = "Olá esta é uma mensagem automática do serviço de reserva da Garbuio, você possui solicitações pendente aguardando sua aprovação.\n Acesse em seu navegador o link para aprovar: http://agenda.garbuio.int"
                # Envia mensagem para lista de contatos
                bot.envia_msg_lista_contatos(lista_contatos, mensagem)
            else:
                print("Não há contato cadastrado no usuário.")
        else:
            print("Não recebeu JSON.")
            
    except KeyboardInterrupt:
        # Finaliza o processo
        print("Usuário parou o processo.")
        bot.finaliza_processo()
    finally:
        # Finaliza o processo e imprime "Fim."
        bot.finaliza_processo()
        print("Fim")
