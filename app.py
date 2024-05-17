from flask import Flask,render_template,redirect,url_for
from moduls import db
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.__init__(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:username>/carrito')
def carrito(username):
    return render_template('carrito.html',username=username)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)