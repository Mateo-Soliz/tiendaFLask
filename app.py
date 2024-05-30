from flask import Flask,render_template,redirect,url_for, request, flash
from moduls import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/imgs'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:username>/carrito')
def carrito(username):
    return render_template('carrito.html',username=username)

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

# Ruta para añadir categoría
@app.route('/add_categoria', methods=['GET', 'POST'])
def add_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        new_categoria = Categoria(nombre=nombre)
        db.session.add(new_categoria)
        db.session.commit()
        return redirect(url_for('add_categoria'))
    return render_template('add_categoria.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)