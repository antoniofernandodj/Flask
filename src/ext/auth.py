from flask_login import LoginManager
from src.models import User
from flask import Flask

def init_app(app: Flask) -> None:
    """Inicializa a extensão de autenticação"""
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int) -> None:
        return User.get(user_id)