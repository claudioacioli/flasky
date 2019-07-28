from flask import render_template
from . import main as app_main


@app_main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app_main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
