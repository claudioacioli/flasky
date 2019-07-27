from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    output = '<h1>Hello World!</h1>'
    output += '<hr />'
    output += '<p>{}</p>'.format(user_agent)
    return output


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Not found!</h1>', 404


@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>Internal Error</h1>', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
