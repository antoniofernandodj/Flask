from sqlalchemy.sql import expression
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    idade = db.Column(db.Integer, unique=True, nullable=False)
    ativo = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    
    @classmethod
    def get(self, id):
        return User.query.filter_by(id=id).first()
    
    def __repr__(self):
        return f'<User {self.nome}>'