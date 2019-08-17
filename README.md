# Flasky
Este projeto foi criado para apredizagem seguindo os capÃ­tulos de 1 a 7, primeira parte, do livro [Desenvolvimento Web com Flask](https://novatec.com.br/livros/desenvolvimento-web-com-flask/)

## Instalação e Execução
Para executar este projeto, após o clone, acesse a pasta do repositório e execute
```
python -m venv venv
```
Certifique-se que o python esta instalado e adicionado a sua variável path.

Instale as dependências com o comando:
```
pip install -r requirements.txt
```

Configure o banco de dados com o comando:
```
flask db upgrade
```

Execute o projeto com>
```
python flasky.py
```

## Utilitario Bash
Para este projeto são criadas algumas variaveis de ambiente. A sugestão seria um arquivo shell ou batch.
Segue conteúdo sugerido:

```
Set SECRET_KEY=sua chave secreta
Set MAIL_SERVER=smtp.googlemail.com
Set MAIL_PORT=587
Set MAIL_USE_TLS=1
Set MAIL_USERNAME=usermail
Set MAIL_PASSWORD=userpassword
Set FLASKY_DEV_DATABASE_URI=data-dev.sqlite
Set FLASKY_ENV=development
SET FLASK_DEBUG=1
Set FLASK_APP=flasky.py
```

## Testes

Os comandos necessários para execução dos testes são os seguintes:

- Ative o ambinte virtual
```
venv\Scripts\activate
```

- Configure as variáveis de ambiente
```
init.bat
```

- Execute o comando de testes
```
flask test
```
