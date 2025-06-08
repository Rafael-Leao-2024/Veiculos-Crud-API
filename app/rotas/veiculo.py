from fastapi import APIRouter, status, Depends
from schema.modelos import Veiculo
from database.sessao_db import get_db

veiculos_db = []

route_veiculos = APIRouter(prefix='/veiculos', tags=['Veiculos'])

@route_veiculos.get('/', response_model=list[Veiculo], status_code=status.HTTP_200_OK)
async def listar_veiculos(cursor=Depends(get_db)):
    cursor.execute('''SELECT * FROM veiculos''')
    veiculos = [dict(id=row[0], marca=row[1], modelo=row[2], ano=row[3], cor=row[4], preco=row[5], is_disponivel=row[6])
                for row in cursor.fetchall()]
    return veiculos


@route_veiculos.get('/{id_veiculo}', response_model=Veiculo)
async def buscar_veiculo(id_veiculo: int, cursor=Depends(get_db)):
    resposta = cursor.execute("SELECT * FROM veiculos WHERE id = '%s'" % id_veiculo)
    veiculo = resposta.fetchone()
    colunas = [desc[0] for desc in cursor.description]
    dados = dict(zip(colunas, veiculo))
    return dados


@route_veiculos.post('/adicionar-veiculo', status_code=status.HTTP_201_CREATED,response_model=Veiculo)
async def adicionar_veiculo(veiculo: Veiculo, cursor=Depends(get_db)):
    sql = '''INSERT INTO veiculos (marca, modelo, ano, cor, preco, is_disponivel)
VALUES (?, ?, ?, ?, ?, ?);
'''
    cursor.execute(sql,  (veiculo.marca, veiculo.modelo, veiculo.ano, veiculo.cor, veiculo.preco, veiculo.is_disponivel))    
    return veiculo


@route_veiculos.put('/atualizar-veiculo/{id_veiculo}', response_model=Veiculo)
async def atualizar_veiculo(id_veiculo: int, veiculo: Veiculo | None = None):
    veiculo_dicionario = veiculo.dict()
    veiculo_encontrado = veiculos_db[id_veiculo -1]
    veiculo_encontrado['marca'] = veiculo_dicionario.get('marca')
    veiculo_encontrado['modelo'] = veiculo_dicionario.get('modelo')
    veiculo_encontrado['ano'] = veiculo_dicionario.get('ano')   
    return veiculo_encontrado


@route_veiculos.delete('/delete/{id_veiculo}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_veiculo(id_veiculo: int, cursor=Depends(get_db)):
    cursor.execute("DELETE FROM veiculos WHERE id = ?", (id_veiculo,))
    return {"message": "Veiculo de ID: {} deletado com sucesso".format(id_veiculo)}


