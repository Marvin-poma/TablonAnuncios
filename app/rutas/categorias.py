from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db, Categoria

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

# 1. Consulta (Listar)
@categorias_bp.route('/')
@login_required
def index():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

# 2 y 3. Registro y Modificación
@categorias_bp.route('/guardar', methods=['POST'])
@categorias_bp.route('/guardar/<int:id>', methods=['POST'])
@login_required
def guardar(id=None):
    if id:
        # Modificar
        categoria = Categoria.query.get_or_404(id)
    else:
        # Crear
        categoria = Categoria()
        
    categoria.nombre = request.form['nombre']
    
    if not id:
        db.session.add(categoria)
        
    db.session.commit()
    flash('Categoría guardada exitosamente', 'success')
    return redirect(url_for('categorias.index'))

# 4. Eliminación
@categorias_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    cat = Categoria.query.get_or_404(id)
    
    # Verificamos que no tenga anuncios asociados para no romper la base de datos
    if len(cat.anuncios) > 0:
        flash('No se puede eliminar la categoría porque tiene anuncios asociados.', 'danger')
    else:
        db.session.delete(cat)
        db.session.commit()
        flash('Categoría eliminada', 'success')
        
    return redirect(url_for('categorias.index'))