from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    # Codigo adicionado mais nao estudado
    # Apos verificar erro no envio de emails analise o codigo do autor do livro
    # Ele adicionou esta linha, talvez nao tenha percebido o pq no decorrer do livro
    app = current_app._get_current_object()
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
