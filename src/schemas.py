from pydantic import BaseModel

class User(BaseModel):
    nome: str
    idade: str
    ativo: bool