from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "db.sqlite3"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'derfgtyhjuik'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db.init_app(app)