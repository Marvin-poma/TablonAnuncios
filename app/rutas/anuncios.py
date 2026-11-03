from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Anuncio, Categoria

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')

@anuncios_bp.route('/')
@login_required
def index():
    anuncios = Anuncio.query.all()
    categorias = Categoria.query.all()
    return render_template('anuncios.html', anuncios=anuncios, categorias=categorias)

@anuncios_bp.route('/crear', methods=['POST'])
@login_required
def crear():
    nuevo = Anuncio(
        titulo=request.form['titulo'],
        contenido=request.form['contenido'],
        usuario_id=current_user.id,
        categoria_id=request.form['categoria_id']
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('anuncios.index'))

@anuncios_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncios.index'))