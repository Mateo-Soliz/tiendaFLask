
from flask import Flask, render_template, redirect, url_for, flash, session, g, request
from flask_wtf import FlaskForm
from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from moduls import *
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static\imgs'
app.config['SECRET_KEY'] = 'clave_secreta'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
db.init_app(app)


class RegistrationForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('El correo electrónico ya está registrado.')

class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)  

@app.route('/')
def index():
    productos = Producto.query.all()
    categorias = Categoria.query.all()
    return render_template('index.html', productos=productos, categorias=categorias)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.nombre.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user , remember=True)
            
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    
    return redirect(url_for('index'))



@app.route('/add_producto', methods=['GET', 'POST'])
def add_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = round(float(request.form['precio']), 2)
        categoria_id = request.form['categoria']
        if 'imagen' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['imagen']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            new_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, categoria_id=categoria_id, imagen=filepath)
            db.session.add(new_producto)
            db.session.commit()
            return redirect(url_for('add_producto'))
    
    categorias = Categoria.query.all()
    return render_template('add_producto.html', categorias=categorias)

@app.route('/add_categoria', methods=['GET', 'POST'])
def add_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        new_categoria = Categoria(nombre=nombre)
        db.session.add(new_categoria)
        db.session.commit()
        return redirect(url_for('add_categoria'))
    return render_template('add_categoria.html')

@app.route('/carrito')
def carrito():
    carritos = Carrito.query.filter_by(username=current_user.username).all()
    productos= []
    coste_Total = 0
    for carrito in carritos:
        producto = Producto.query.filter_by(nombre=carrito.producto_nombre).first()
        productos.append({'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio, 'cantidad': carrito.cantidad, 'total': carrito.total, 'imagen': producto.imagen, 'id': carrito.id})
        coste_Total += carrito.total
    print(productos)
    return render_template('carrito.html', productos=productos, coste_Total=coste_Total)

@app.route('/add_carrito/<int:id>', methods=['GET', 'POST'])
@login_required
def add_carrito(id):
    if request.method == 'POST':
        product = Producto.query.get(id)
        cantidad = int(request.form['cantidad'])
        total = float(cantidad * product.precio)
        allCarritos = len(Carrito.query.all())
        id = allCarritos + 1
        new_carrito = Carrito(id=id,username=current_user.username, producto_nombre=product.nombre, cantidad=cantidad, total=total)
        db.session.add(new_carrito)
        db.session.commit()
        return redirect(url_for('carrito'))
    product = Producto.query.get(id)
    return render_template('add_carrito.html', producto=product)

@app.route('/delete_carrito/<int:id>', methods=['GET', 'POST'])
def delete_carrito(id):
    carrito = Carrito.query.filter_by(id=id).first()
    if carrito:
        db.session.delete(carrito)
        db.session.commit()
        return redirect(url_for('carrito'))
    return redirect(url_for('carrito'))

@app.route('/comprar')
def comprar():
    carritos = Carrito.query.filter_by(username=current_user.username).all()
    for carrito in carritos:
        db.session.delete(carrito)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)