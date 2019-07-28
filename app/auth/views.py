from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user
from . import auth as app_auth
from ..models import User
from .forms import LoginForm


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
