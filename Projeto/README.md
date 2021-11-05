# Projeto - Site de Leilões 🔨

## Como rodar o projeto? 👨‍💻

### Instale os pacotes necessários 🔽

O projeto atual só precisa de um único pacote Python "Django", ele foi construído e testado com a versão Django 2.x. Para instalá-lo, use o seguinte comando:

    pip install -r requirements.txt

O projeto requer Python 3, se você precisar de ajuda para configurar Python 3 em sua máquina, você pode consultar a excelente documentação DigitalOcean sobre
[Como instalar e configurar um ambiente de programação local para Python 3](https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3)

### Instale o MySQLServer 💾

Para gerenciar o banco de dados do projeto, é necessário instalar o programa MySQLServer, que pode ser obtido para Linux a partir do [seguinte tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04-pt), e para Windows a partir do [seguinte link](https://www.mysqltutorial.org/install-mysql/).

### Configure o banco de dados 🎲

Primeiramente, devem ser criadas as bases de dados utilizadas no projeto:

```sql
CREATE DATABASE leilaoDB;
CREATE DATABASE test_leilaoDB;
```

Em seguida, cria-se o usuário de acessoa o projeto com as permissões concedidas às bases de dados:

```sql
CREATE USER PCS3643@localhost IDENTIFIED BY 'caibardo123';
GRANT ALL PRIVILEGES ON leilaoDB.* TO PCS3643@localhost;
GRANT ALL PRIVILEGES ON test_leilaoDB.* TO PCS3643@localhost;
FLUSH PRIVILEGES;
```

Por fim, precisamos criar as tabelas de banco de dados necessárias:

    python manage.py makemigrations 
    python manage.py migrate


### Preciso de um usuário e senha para acessar "catalogo" 🔑

Para criar um super usuário, basta utilizar o seguinte comando:

    python manage.py createsuperuser

Para criar um usuário normal (não superusuário), você deve fazer login na página de administração e criá-lo
: <http://localhost:8000/admin/>

### Executando o aplicativo 🖱️

Agora você pode executar o servidor de desenvolvimento da web:

    python manage.py runserver

Para acessar no aplicativo vá para o URL <http://localhost:8000/>

## Como rodar testes automatizados? ✅

### Testes Unitários 🧱

Para rodar testes unitários, use o comando abaixo:

    python manage.py test --noinput

Caso o aviso abaixo seja exibido no terminal, basta escolher a opção `yes`.

```
Got an error creating the test database: (1007, "Can't create database 'test_leilaoDB'; database exists")
Type 'yes' if you would like to try deleting the test database 'test_leilaoDB', or 'no' to cancel:
```

### Testes de Interface 📲

Para rodar os testes de interface, deve-se utilizar o Selenium. Estando no Selenium IDE, basta abrir o arquivo `teste_interface.side`, que se encontra na pasta `Projeto` deste repositório e rodar os testes de interface. Tais testes cobrem as principais funcionalidades de login e gerenciamento de leilões, lotes e lances.

❗ É importante que haja um superusuário chamado `berbardo` com a senha `berbardo123`

⚠️ Certifique-se de que você esteja deslogado ao rodar os testes. Todos os testes fazem um login no início e um logout no fim.