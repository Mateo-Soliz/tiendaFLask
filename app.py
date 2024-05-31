
from flask import Flask, render_template, redirect, url_for, flash, session, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
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

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.nombre.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Felicidades, ya estás registrado!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.username
            flash('¡Has iniciado sesión!')
            return redirect(url_for('index'))
        else:
            flash('Correo electrónico o contraseña incorrectos')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Has cerrado sesión.')
    return redirect(url_for('index'))

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id else None



@app.route('/add_producto', methods=['GET', 'POST'])
def add_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
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
    

    return render_template('carrito.html')

@app.route('/add_carrito/<int:id>', methods=['GET', 'POST'])
def add_carrito():
    if request.method == 'POST':
        product = Producto.query.get(id)
        cantidad = request.form['cantidad']
        total = cantidad * product.precio
        new_carrito = Carrito(username=g.user.username, producto_nombre=product.nombre, cantidad=cantidad, total=total)
        db.session.add(new_carrito)
        db.session.commit()
        return redirect(url_for('carrito'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)