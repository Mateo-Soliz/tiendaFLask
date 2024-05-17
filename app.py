from flask import Flask,render_template,redirect,url_for
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:username>/carrito')
def carrito(username):
    return render_template('carrito.html',username=username)


if __name__ == '__main__':
    app.run(debug=True)