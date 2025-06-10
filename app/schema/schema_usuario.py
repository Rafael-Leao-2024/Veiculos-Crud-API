from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    nome: str
    email:str
    disabled: Optional[bool] = False
    senha: str

class UsuarioInDB(Usuario):
    id: int
        
class UsuarioOutput(BaseModel):
    id:int
    nome: str
    email:str
    disabled: Optional[bool] = False