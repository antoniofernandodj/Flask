from flask import Flask

from src.ext import config
from src.ext import database
from src.ext import auth
from src import views

def create_app() -> Flask:
    """Cria a instância principal da aplicação"""
    app = Flask(__name__)

    auth.init_app(app)
    config.init_app(app)
    database.init_app(app)
    views.init_app(app)
    
    return app