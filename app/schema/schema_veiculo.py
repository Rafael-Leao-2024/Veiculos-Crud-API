from pydantic import BaseModel


class Veiculo(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: int
    cor: str | None = None
    preco: float | None = None
    is_disponivel : bool = True


class VeiculoUpdate(BaseModel):
    marca: str
    modelo: str
    ano: int
    cor: str | None = None
    preco: float | None = None
    is_disponivel : bool = True





