from pydantic import BaseModel

class User(BaseModel):
    nome: str
    senha: str
