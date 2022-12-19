from typing import Dict, Union, List, Optional
from flask.views import View


def path(
    route: str, view_function: callable, methods: Optional[List[str]] = None
) -> Dict[str, Union[str, callable, List[str]]]:
    """Retorna um objeto usado para cadastro de rotas da aplicação Flask"""
    return {'route': route, 'func': view_function, 'methods': methods}
