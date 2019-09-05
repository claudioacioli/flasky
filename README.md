# Flasky
Este projeto foi criado seguindo o livro [Desenvolvimento Web com Flask](https://novatec.com.br/livros/desenvolvimento-web-com-flask/)

## Instalação e Execução
Para executar este projeto, após o clone, acesse a pasta do repositório e execute
```
 $ python -m venv venv
```
Certifique-se que o python esta instalado e adicionado a sua variável path.

Instale as dependências com o comando:
```
(venv) $ pip install -r requirements.txt
```

Inicialize o banco de dados com o comando:
```
(venv) $ flask db upgrade
```

Execute o projeto com:
```
(venv) $ python flasky.py
```

## Utilitario Bash
Para este projeto são criadas algumas variaveis de ambiente. A sugestão seria um arquivo shell ou batch.
Segue conteúdo sugerido:

```
SET SECRET_KEY=sua chave secreta
SET MAIL_SERVER=smtp.googlemail.com
SET MAIL_PORT=587
SET MAIL_USE_TLS=1
SET MAIL_USERNAME=usermail
SET MAIL_PASSWORD=userpassword
SET FLASKY_DEV_DATABASE_URI=sqlite:///C:\\flasky\\data-dev.sqlite
SET FLASK_ENV=development
SET FLASK_DEBUG=1
SET FLASK_APP=flasky.py
SET FLASKY_ADMIN=admin@email.com
```

## Testes

Os comandos necessários para execução dos testes são os seguintes:

- Ative o ambinte virtual
```
(venv) $ venv\Scripts\activate
```

- Configure as variáveis de ambiente
```
(venv) $ init.bat
```

- Execute o comando de testes
```
(venv) $ flask test
```

## Migrate

Ao alterar as classes de modelo, é necessário gerar as "migrations", por tanto use o seguinte comando

```
(venv) $ flask db migrate -m"adiciona uma mensagem relevante a alteração de banco de dados"
```

Após esse passo, é necessário atualizar o banco com o seguinte comando:
```
(venv) $ flask db upgrade
```

## Faker

A dependência de projeto ``faker`` ajuda a criar usuarios e postagens fake. 
Após instalar a dependência, execute os comandos:

```
// Atenção, código copiado da página 183
(venv) $ flask shell
>>> from app import fake
>>> fake.users(100)
>>> fake.posts(100)
```
