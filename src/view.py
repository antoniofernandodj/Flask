from . import app
from .models import User
from flask import render_template
from os import getpid

class ClientView:
    def __init__(self, username):
        with app.app_context():
            self.user = User.query.filter_by(username=username).first()
            self.users = User.query.all()
        
    def index(self):
        return render_template(
            'index.jinja2.html',
            user = self.user,
            users = self.users
        )
        
class LoginView:
    def __init__(self):
        self.pid = getpid()
    
    def login(self):
        return render_template(
            'login.jinja2.html',
            pid = self.pid
        )