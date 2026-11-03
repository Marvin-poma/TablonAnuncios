from flask import Flask
from flask_login import LoginManager
from .models import db, Usuario

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'otra-clave-distinta-456'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablon_v2.db'
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar Blueprints
    from .rutas.auth import auth_bp
    from .rutas.anuncios import anuncios_bp
    from .rutas.categorias import categorias_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(categorias_bp)

    # Crear BD y Usuario Admin
    with app.app_context():
        db.create_all()
        if not Usuario.query.first():
            admin = Usuario(username="admin")
            admin.set_password("1234")
            db.session.add(admin)
            db.session.commit()

    return app