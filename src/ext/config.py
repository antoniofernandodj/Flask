from flask import Flask

def init_app(app: Flask) -> None:
    DB_NAME = "db.sqlite3"
    app.config['SECRET_KEY'] = 'derfgtyhjuik'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'