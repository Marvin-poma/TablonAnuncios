from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import db, Usuario

auth_bp = Blueprint('auth', __name__)

# --- LOGIN ---
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('anuncios.index'))
        flash('Datos incorrectos', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# --- CRUD DE USUARIOS (Punto 4 del PDF) ---

# 1. Consulta (Listar)
@auth_bp.route('/usuarios/')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista_usuarios)

# 2 y 3. Registro y Modificación (Crear y Editar)
@auth_bp.route('/usuarios/guardar', methods=['POST'])
@auth_bp.route('/usuarios/guardar/<int:id>', methods=['POST'])
@login_required
def guardar_usuario(id=None):
    if id:
        # Modificar
        usuario = Usuario.query.get_or_404(id)
    else:
        # Crear
        usuario = Usuario()

    usuario.username = request.form['username']
    
    # Solo actualizar contraseña si se escribió una nueva
    if request.form['password']:
        usuario.set_password(request.form['password'])
        
    if not id:
        db.session.add(usuario)
        
    db.session.commit()
    flash('Usuario guardado exitosamente', 'success')
    return redirect(url_for('auth.usuarios'))

# 4. Eliminación
@auth_bp.route('/usuarios/eliminar/<int:id>')
@login_required
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    # Evitar que el admin se elimine a sí mismo
    if usuario.id != 1: 
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado', 'success')
    else:
        flash('No puedes eliminar al administrador principal', 'danger')
    return redirect(url_for('auth.usuarios'))