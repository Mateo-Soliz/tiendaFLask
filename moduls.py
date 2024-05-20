from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
db = SQLAlchemy()


class user(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    carrito = db.relationship('carrito', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

class carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), ForeignKey('user.username'))
    producto = db.Column(db.String(80), ForeignKey('producto.nombre'))
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Carrito %r>' % self.username

class producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    precio = db.Column(db.Float(10,2), nullable=False)
    carrito = db.relationship('carrito', backref='carrito', lazy=True)

    def __repr__(self):
        return '<Producto %r>' % self.username

class pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), ForeignKey('user.username'))
    producto = db.Column(db.String(80), ForeignKey('producto.nombre'))
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Pedido %r>' % self.username
    
    