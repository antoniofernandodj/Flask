from src.models import User
from src.models import db
from flask import Flask
from src.config import settings

def init_app(app: Flask) -> None:
    """Inicializa o banco de dados"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        user = User(nome=settings.USERNAME, senha=settings.PASSWORD)
        item = db.session.query(User).filter_by(nome='Antonio').first()
        if not item:
            user.save()
