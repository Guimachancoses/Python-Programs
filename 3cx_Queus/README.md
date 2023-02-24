# Selenium Web Automation for 3CX

Este projeto contém um web scraper construído em Python utilizando a biblioteca Selenium. O objetivo deste web scraper é automatizar a navegação e a inserção dos usuários em uma fila de modo automático, de um sistema de atendimento de chamados 3CX.

O código está organizado em módulos, que podem ser encontrados na pasta app/modules. Cada módulo tem uma funcionalidade específica e pode ser utilizado em outros projetos de web scraping.

* Módulos

1. ChromeDriverSelenium.py

    Este módulo é responsável por atualizar o driver do Chrome utilizado pelo Selenium para a versão mais recente disponível. Ele verifica a versão do Chrome instalada no sistema operacional e faz o download do driver compatível com essa versão. Em seguida, ele move o arquivo executável do driver para o PATH do sistema, permitindo que o Selenium o utilize.

2. queues.py

    Este módulo é responsável por navegar no sistema de atendimento de chamados e coletar informações sobre as filas de atendimento. Ele faz o login no sistema e navega até a  página de filas de atendimento. Em seguida, ele coleta informações sobre cada fila, como o número de chamados em espera e o tempo médio de espera.

* Dependências

O projeto utiliza as seguintes bibliotecas Python:

. Selenium
. webdriver_manager
. time
. Para instalar as dependências, execute o seguinte comando no terminal:

pip install -r requirements.txt

* Executando o código

Para executar o código, basta executar o arquivo main.py na pasta raiz do projeto. Certifique-se de ter as dependências instaladas antes de executar o código.

python main.py

* Autor

Este projeto foi criado por Guilherme Machancoses.

* Licença

Este código é licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.
