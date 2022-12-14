from .views.view import (
    ClientView,
    LoginView
)


url_rules = [
    {'route': "/users/", 'func': ClientView.as_view("user_list"), 'methods': ['GET'] },
    {'route': '/login/', 'func': LoginView.as_view("login_user"), 'methods': ['GET', 'POST'] }
]
