from flask import render_template, request
from os import getpid
from flask_login import login_user
from flask.views import View
from src import schemas
from src import models
from src.models import db


class ClientView(View):
    def dispatch_request(self):
        users = models.User.query.all()
        return render_template('index.html',users=users)

class LoginView(View):
    def __init__(self):
        methods = ['GET', 'POST']
        self.pid = getpid()
        
    def dispatch_request(self):
        
        if request.method == 'POST':
            user_schema = schemas.User(
                nome=request.form['nome'],
                idade=request.form['idade'],
                ativo=request.form['ativo']
            )
            user = models.User(**user_schema.dict())
            db.session.add(user)
            db.session.commit()
            db.session.close()
        
        return render_template('login.html', pid=self.pid)