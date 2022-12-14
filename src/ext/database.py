from src.models import User
from src.models import db
from flask import Flask

def init_app(app: Flask) -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
        user = User(nome='admin', idade=25, ativo=True)
        item = db.session.query(User).filter_by(nome='admin').first()
        if not item:
            db.session.add(user)
            db.session.commit()
            db.session.close()