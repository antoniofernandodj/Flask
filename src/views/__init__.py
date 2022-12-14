from src.urls import url_rules
from flask import Flask

def init_app(app: Flask) -> None:
    for rule in url_rules:
        app.add_url_rule(
            rule=rule.get('route'),
            view_func=rule.get('func'),
            methods=rule.get('methods')
        )