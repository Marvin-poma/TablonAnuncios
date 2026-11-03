from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import db, Usuario, Categoria, Anuncio

main_bp = Blueprint('main', __name__)

# --- LOGIN ---
@main_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(nombre=request.form['nombre']).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('main.tablero'))
    return render_template('login.html')

# --- TABLERO (Anuncios y Categorías) ---
@main_bp.route('/tablero', methods=['GET', 'POST'])
def tablero():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        # Crear Anuncio
        nuevo = Anuncio(
            titulo=request.form['titulo'],
            contenido=request.form['contenido'],
            usuario_id=session['user_id'],
            categoria_id=request.form['categoria_id']
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('main.tablero'))

    anuncios = Anuncio.query.all()
    categorias = Categoria.query.all()
    return render_template('tablero.html', anuncios=anuncios, categorias=categorias)

# --- CREAR CATEGORÍA ---
@main_bp.route('/categoria', methods=['POST'])
def crear_categoria():
    if 'user_id' in session:
        nueva = Categoria(nombre=request.form['nombre'])
        db.session.add(nueva)
        db.session.commit()
    return redirect(url_for('main.tablero'))

# --- ELIMINAR (Usuario, Categoría, Anuncio) ---
@main_bp.route('/eliminar/<tipo>/<int:id>')
def eliminar(tipo, id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    if tipo == 'anuncio':
        item = Anuncio.query.get(id)
    elif tipo == 'categoria':
        item = Categoria.query.get(id)
    elif tipo == 'usuario':
        item = Usuario.query.get(id)
        
    if item:
        db.session.delete(item)
        db.session.commit()
    
    return redirect(url_for('main.tablero'))

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))