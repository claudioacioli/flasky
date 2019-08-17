from datetime import datetime

from flask import \
    render_template,\
    session,\
    redirect,\
    url_for,\
    current_app
from . import main as app_main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email


@app_main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['know'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New user', 'mail/new_user', user=user)
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        redirect(url_for('.index'))
    return render_template(
        'index.html',
        current_time=datetime.utcnow(),
        form=form,
        name=session.get('name'),
        know=session.get('know', False)
    )


@app_main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
