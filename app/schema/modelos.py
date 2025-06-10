from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id: int
    nome: str
    email:str
    disabled: Optional[bool] = None

class UsuarioInDB(Usuario):
    senha: str
    

class Veiculo(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: int
    cor: str | None = None
    preco: float | None = None
    is_disponivel : bool = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str]


