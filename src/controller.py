from . import view

# Instance of a view class
client = view.ClientView(username='admin')
lg = view.LoginView()

url_rules = [
    {'route': '/home', 'func': client.index, 'methods': ['GET'] },
    {'route': '/login', 'func': lg.login, 'methods': ['GET'] }
]
