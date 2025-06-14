from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    nome: str
    email:str
    disabled: Optional[bool] = False
    senha: str

    class Config:
        json_schema_extra = {
            "examples":[
                {
                    "nome": "Seu nome Completo",
                    "email": "email valido",
                    "disabled": False,
                    "senha": "Senha"
                }
            ]
        }


class UsuarioInDB(Usuario):
    id: int
        
class UsuarioOutput(BaseModel):
    id:int
    nome: str
    email:str
    disabled: Optional[bool] = False