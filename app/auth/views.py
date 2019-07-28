from flask import render_template
from . import auth as app_auth


@app_auth.route('/login')
def login():
    return render_template('auth/login.html')
