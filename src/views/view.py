from flask import render_template, request, redirect, url_for, flash
from os import getpid
from flask_login import login_user
from flask.views import View
from src import schemas
from src import models
from src.models import db
from src.libs import tasks
from crontab import CronTab
from pathlib import Path
from flask import typing as ft
import os
from flask_login import login_required, logout_user


PROJECT_PATH = str(Path(__file__).parent.parent)
CRON_PATH = os.path.join(PROJECT_PATH, 'tabs', 'crontab')
DEFAULT_CRON_PATH = os.path.join(PROJECT_PATH, 'tabs', 'defaulttab')

# set this to use the main cron
# CRON_PATH = '/etc/crontab'


class Jobs(View):
    decorators = [login_required]
    
    def dispatch_request(self):
        cron = CronTab(tabfile=CRON_PATH, user=True)
        return render_template(
            'index.html',
            cron=cron,
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
            
            minutes = request.form.get('minutes')
            hours = request.form.get('hours')
            day = request.form.get('days')
            months = request.form.get('months')
            dow = request.form.getlist('dow')
            user = request.form.get('user')
            
            command = request.form.get('command')
            comment = request.form.get('comment')
            
            cron = CronTab(tabfile=CRON_PATH, user='root')
                
            job = cron.new(
                command=f'root\t{command}',
                comment=f'{comment}',
                user=True)
            
            if minutes:
                job.minutes.every(int(minutes))
            if hours:
                job.hours.every(int(hours))
            if day:
                job.day.every(int(day))
            if months:
                job.months.every(int(months))
            if dow:
                job.dow.on(*dow)
                
            cron.write()
        return redirect(url_for('jobs'))


class DelJob(View):
    method = ['GET']
    decorators = [login_required]
    
    def dispatch_request(self, index) -> ft.ResponseReturnValue:
        cron = CronTab(tabfile=CRON_PATH, user=True)
        job = cron[index]
        cron.remove(job)
        job.clear()
        cron.write()
        return redirect(url_for('jobs'))


class ResetToDefault(View):
    method = ['GET']
    decorators = [login_required]
    
    def dispatch_request(self) -> ft.ResponseReturnValue:
        with open(DEFAULT_CRON_PATH) as f: content = f.readlines()
        with open(CRON_PATH, 'w') as f: f.write(''.join(content))
        return redirect(url_for('jobs'))


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

