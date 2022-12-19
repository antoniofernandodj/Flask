from sqlalchemy.sql import expression
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash, gen_salt
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    
    @classmethod
    def get(self, id):
        return User.query.filter_by(id=id).first()
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.nome}>'
    
    def save(self):
        self.senha = generate_password_hash(self.senha)
        db.session.add(self)
        db.session.commit()
        db.session.close()
    
    def validate_credentials(self):
        user = User.query.filter_by(nome=self.nome).first()
        valid_credentials =  check_password_hash(user.senha, self.senha)
        return user if valid_credentials else None
