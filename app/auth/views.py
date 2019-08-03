from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth as app_auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm


@app_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Usuario inválido')
    return render_template('auth/login.html', form=form)


@app_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.')
    return redirect(url_for('main.index'))


@app_auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        send_email(
            user.email,
            'Confirme sua conta no Flasky',
            'auth/email/confim',
            user=user,
            token=token
        )
        flash('Um email de confirmacao foi enviado para voce!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@app_auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Parabens! conta confirmada')
    else:
        flask('Link de confirmacao invalido')
    return redirect(url_for('main.index'))

