from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    carritos = db.relationship('Carrito', backref='user', lazy=True)
    pedidos = db.relationship('Pedido', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float(10, 2), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    imagen = db.Column(db.String(120), nullable=False)
    carritos = db.relationship('Carrito', backref='producto', lazy=True)
    pedidos = db.relationship('Pedido', backref='producto', lazy=True)

    def __repr__(self):
        return '<Producto %r>' % self.nombre

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False, unique=True)
    productos = db.relationship('Producto', backref='categoria_rel', lazy=True)

    def __repr__(self):
        return '<Categoria %r>' % self.nombre

class Carrito(db.Model):
    __tablename__ = 'carrito'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), primary_key=True)
    producto_nombre = db.Column(db.String(80), db.ForeignKey('producto.nombre'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return '<Carrito %r, %r, %r>' % (self.id, self.username, self.producto_nombre)

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), db.ForeignKey('user.username'))
    producto_nombre = db.Column(db.String(80), db.ForeignKey('producto.nombre'))
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Pedido %r>' % self.id
