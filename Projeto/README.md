# Projeto - Site de Leilões 🔨

## Instale os pacotes necessários

O projeto atual só precisa de um único pacote Python "Django", ele foi construído e testado com a versão Django 2.x. Para instalá-lo, use o seguinte comando:

    pip install -r requirements.txt

Django 2 requer Python 3, se você precisar de ajuda para configurar Python 3 em sua máquina, você pode consultar a excelente documentação DigitalOcean sobre
[Como instalar e configurar um ambiente de programação local para Python 3] (https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment- for-python-3)

## Executando o aplicativo

Antes de executar o aplicativo, precisamos criar as tabelas de banco de dados necessárias:

    ./manage.py migrate

Agora você pode executar o servidor de desenvolvimento da web:

    ./manage.py runserver

Para acessar no aplicativo vá para o URL <http://localhost:8000/>

## Preciso de um usuário e senha para acessar "catalogo"

Para criar um super usuário, basta utilizar o seguinte comando:

    ./manage.py createsuperuser

Para criar um usuário normal (não superusuário), você deve fazer login na página de administração e criá-lo
: <http://localhost:8000/admin/>
