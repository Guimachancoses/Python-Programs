from Controller.insertTelemetria import MainTelemetria
from Controller.insertAlarm import MainAlarm
from Controller.insertMacros import MainMacros
from Controller.insertPosicao import MainPosicao

if __name__ == '__main__':
    
    reg = 0

    # Obtem os dados da Telemetria e grava no banco de dados
    tlCount = MainTelemetria()
    reg += tlCount
    

    # Obtem os dados da Alarm e grava no banco de dados
    alCount = MainAlarm()
    reg += alCount
    
    
    # Obtem os dados da Macros e grava no banco de dados
    MacCount = MainMacros()
    reg += MacCount
    
    
    # Obtem os dados da Posicao e grava no banco de dados
    PosiCount = MainPosicao()
    reg += PosiCount
    
    print("------------------------------------------------------")
    print(f"Total de dados inseridos em telemetria: {tlCount}")
    print("------------------------------------------------------")
    print(f"Total de dados inseridos em Alarm: {alCount}")    
    print("------------------------------------------------------")
    print(f"Total de dados inseridos em Macros: {MacCount}")
    print("------------------------------------------------------")
    print(f"Total de dados inseridos em Posições: {PosiCount}")    
    print("------------------------------------------------------")
    print(f'Total de registros gravados: {reg}')
