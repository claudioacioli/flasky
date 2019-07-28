from datetime import datetime

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from forms import NameForm

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Configura chave secreta
app.config['SECRET_KEY'] = 'Hard to guees string'


@app.route('/', methods=['GET', 'POST'])
def index():
    user_agent = request.headers.get('User-Agent')
    print(user_agent)
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template(
        'index.html',
        current_time=datetime.utcnow(),
        form=form,
        name=name
    )


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
