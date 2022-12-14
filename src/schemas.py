from pydantic import BaseModel

class User(BaseModel):
    nome: str
    idade: int
    ativo: bool