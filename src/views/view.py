from flask import render_template, request, redirect, url_for, flash
from os import getpid
from flask_login import login_user
from flask.views import View
from src import schemas
from src import models
from src.models import db
from src.libraries import tasks
from crontab import CronTab
from pathlib import Path
from flask import typing as ft
import os
from flask_login import login_required, logout_user


PROJECT_PATH = str(Path(__file__).parent.parent)
DEFAULT_CRON_PATH = os.path.join(PROJECT_PATH, 'tabs', 'defaulttab')

HOME = os.getenv('HOME')
CRON_PATH = '/etc/crontab'


class Jobs(View):
    decorators = [login_required]
    
    def dispatch_request(self):
        user = request.args.get('user')
        
        if not user:
            return render_template(
                'index.html',
                cron='', user='', usernotfound='',
                enumerate=enumerate, str=str
            )
        
        usernotfound = ''
        try:
            cron = CronTab(tabfile=CRON_PATH, user=True)
            
        except FileNotFoundError:
            with open(CRON_PATH, 'w') as f: f.write('#\n')
            cron = CronTab(tabfile=CRON_PATH, user=True)
            
        except IsADirectoryError:
            cron = CronTab(tabfile=CRON_PATH, user=True)
            usernotfound = user
            user = ''
        
        return render_template(
            'index.html',
            cron=cron,
            user=user,
            usernotfound=usernotfound,
            enumerate=enumerate, str=str
        )


class RunCron(View):
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self) -> ft.ResponseReturnValue:
        print('Will run scheduler now...')
        tab = CronTab(tabfile=CRON_PATH)
        for result in tab.run_scheduler():
            print(result)
        return ''


class LongRequest(View):
    def dispatch_request(self) -> ft.ResponseReturnValue:
        tasks.long_task.delay()
        return 'calculando'


class NewJob(View):
    methods = ['GET', 'POST']
    decorators = [login_required]
    
    def dispatch_request(self) -> ft.ResponseReturnValue:

        if request.method == 'POST':

            user = request.form.get('user')

            minutes = request.form.get('minutes')
            hours = request.form.get('hours')
            day = request.form.get('days')
            months = request.form.get('months')
            dow = request.form.getlist('dow')
            user = request.form.get('user')
            
            command = request.form.get('command')
            comment = request.form.get('comment')
            
            minutes = minutes if minutes else '*'
            hours = hours if hours else '*'
            day = day if day else '*'
            months = months if months else '*'
            dow = str(dow) \
                .replace("[", "") \
                .replace("]", "") \
                .replace("'", "") \
                .replace(" ", "") if dow else '*'
                
            user = user if user else '*'
            comment = comment if comment else ''
            
            string = f"{minutes} {hours} {day} {months} {dow} {user}\t{command} # {comment}"
            
            with open(CRON_PATH, 'a') as f:
                f.write(f'{string}\n')
            
        return redirect(request.referrer)


class DelJob(View):
    method = ['GET']
    decorators = [login_required]
    
    def dispatch_request(self, index, user) -> ft.ResponseReturnValue:
        tabfile = CRON_PATH
        cron = CronTab(tabfile=tabfile, user=True)
        job = cron[index]
        cron.remove(job)
        job.clear()
        cron.write()
        return redirect(request.referrer)


class ResetToDefault(View):
    method = ['GET']
    decorators = [login_required]
    
    def dispatch_request(self) -> ft.ResponseReturnValue:
        with open(DEFAULT_CRON_PATH) as f: content = f.readlines()
        with open(CRON_PATH, 'w') as f: f.write(''.join(content))
        return redirect(request.referrer)


class Login(View):
    methods = ['GET', 'POST']
    def __init__(self):
        self.pid = getpid()
    
    def dispatch_request(self):
        if request.method == 'POST':
            user_schema = schemas.User(
                nome=request.form['nome'],
                senha=request.form['senha'])
            
            user = models.User(**user_schema.dict()).validate_credentials()
            if user:
                login_user(user=user)
                return redirect(url_for('jobs'))
            
            flash('Credenciais inválidas', category="erro")
        
        return render_template(
            'login.html',
            pid=self.pid
        )


class Logout(View):
    def dispatch_request(self) -> ft.ResponseReturnValue:
        logout_user()
        return redirect(url_for('login'))

