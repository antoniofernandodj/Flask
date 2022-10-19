from . import app
from .models import User
from flask import render_template
from os import getpid
from flask_login import login_user

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

	def login2(self):
		form = LoginForm()
		if form.validate_on_submit():
			login_user(user)

			flask.flash('Logged in successfully.')

			next = flask.request.args.get('next')
			if not is_safe_url(next):
				return flask.abort(400)

			return flask.redirect(next or flask.url_for('index'))
		return flask.render_template('login.html', form=form)
