from fastapi import APIRouter, status
from schema.modelos import Veiculo
from database.banco_fake import veiculos_db

route_veiculos = APIRouter(prefix='/veiculos', tags=['Veiculos'])


@route_veiculos.get('/', response_model=list[Veiculo])
async def listar_veiculos():
    return veiculos_db


@route_veiculos.get('/{id_veiculo}', response_model=Veiculo)
async def buscar_veiculo(id_veiculo: int):
    return veiculos_db[id_veiculo -1]


@route_veiculos.post('/adicionar-veiculo', status_code=status.HTTP_201_CREATED,response_model=Veiculo)
async def adicionar_veiculo(veiculo: Veiculo):
    veiculo.id = len(veiculos_db)
    veiculos_db.append(veiculo)
    return veiculo


@route_veiculos.put('/atualizar-veiculo/{id_veiculo}', response_model=Veiculo)
async def atualizar_veiculo(id_veiculo: int, veiculo: Veiculo | None = None):
    veiculo_dicionario = veiculo.dict()
    veiculo_encontrado = veiculos_db[id_veiculo -1]
    veiculo_encontrado['marca'] = veiculo_dicionario.get('marca')
    veiculo_encontrado['modelo'] = veiculo_dicionario.get('modelo')
    veiculo_encontrado['ano'] = veiculo_dicionario.get('ano')   
    return veiculo_encontrado


@route_veiculos.delete('/delete/{id_veiculo}')
async def deletar_veiculo(id_veiculo: int):
    veiculo = veiculos_db[id_veiculo]
    veiculos_db.pop(id_veiculo)
    return {"message": f"Veiculo deletado com sucesso {veiculo}"}


