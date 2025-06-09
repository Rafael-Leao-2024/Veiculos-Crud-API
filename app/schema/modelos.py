from pydantic import BaseModel


class Usuario(BaseModel):
    id: int
    nome: str
    email:str

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



