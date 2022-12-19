from flask import Flask
from src.config import settings

def init_app(app: Flask) -> None:
    """Inicializa as configurações da aplicação"""
    app.config['SECRET_KEY'] = settings.FLASK_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI