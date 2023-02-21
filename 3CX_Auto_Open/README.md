3CX Desktop App Launcher

Esse programa verifica se a aplicação 3CX Desktop App está em execução no computador e, caso não esteja, inicia a aplicação.

Instalação

1. Clone ou baixe este repositório.
2. Navegue até a pasta raiz do projeto e execute o seguinte comando:

python setup.py install

Utilização

Para utilizar o programa, abra o terminal (ou prompt de comando) e execute o comando 3cx-app-launcher. O programa verificará se a aplicação 3CX Desktop App está em execução e a iniciará caso não esteja.

Você também pode passar um nome de usuário específico para a função check_and_launch_app, caso deseje instalar a aplicação em um usuário diferente. Para isso, utilize o comando 3cx-app-launcher-user, seguido do nome de usuário desejado:

3cx-app-launcher-user "outro_usuario"

Contribuindo
Se você quiser contribuir para este projeto, por favor:

1. Fork o repositório
2. Crie uma nova branch (git checkout -b feature/minha-nova-feature)
3. Commit suas mudanças (git commit -am 'Adiciona minha nova feature')
4. Faça o push para a branch (git push origin feature/minha-nova-feature)
5. Abra um Pull Request

Licença

Este projeto é licenciado sob a MIT License. Veja o arquivo LICENSE para mais informações.