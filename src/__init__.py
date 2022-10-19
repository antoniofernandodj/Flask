from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
db = SQLAlchemy()
DB_NAME = "db.sqlite3"
app = Flask(__name__)
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'derfgtyhjuik'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


