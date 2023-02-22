# Calculadora de Distâncias com Google Maps

Este código é uma calculadora de distâncias que usa a API do Google Maps para calcular a distância entre cada par de coordenadas em uma planilha de Excel e adiciona uma nova coluna com as distâncias calculadas.

* Pré-requisitos

Antes de usar este código, você precisará instalar o Python 3 e as seguintes bibliotecas Python:

googlemaps
pandas

* Instalação

Para instalar as dependências, execute o seguinte comando:

pip install -r requirements.txt

* Como usar

Para usar este código, siga estas etapas:

1. Obtenha uma chave da API do Google Maps e substitua 'sua_chave_de_API' em distancias.py pela sua chave.

2. Salve sua planilha de coordenadas em um arquivo de Excel (.xlsx) e especifique o caminho do arquivo e o nome da planilha em    distancias.py.

3. Execute o seguinte comando:

    python main.py

O resultado será uma nova planilha com uma coluna adicional contendo as distâncias calculadas.

* Licença

Este código é licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.
