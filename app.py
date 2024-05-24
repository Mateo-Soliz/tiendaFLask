from flask import Flask,render_template,redirect,url_for
from moduls import db,User,Producto,Carrito,Pedido
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:username>/carrito')
def carrito(username):
    return render_template('carrito.html',username=username)

@app.route('/login' , methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/logout' , methods=['GET'])
def logout():
    return redirect(url_for('index'))

@app.route('/register' , methods=['GET'])
def register():
    return render_template('register.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)