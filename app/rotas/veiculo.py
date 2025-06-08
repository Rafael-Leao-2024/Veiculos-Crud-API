from fastapi import APIRouter, status, Depends, HTTPException
from app.schema.modelos import Veiculo
from app.database.sessao_db import get_db



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

@route_veiculos.get('/is-locado/', status_code=status.HTTP_200_OK)
async def is_disponivel(locado: int, cursor=Depends(get_db)):
    if locado > 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escolha 0 para ver os veiculos locados ou 1 para ver os disponiveis!")  
    cursor.execute("""
SELECT * FROM veiculos WHERE is_disponivel = ?""", (locado, ))    
    is_locados = [dict(id=row[0], marca=row[1], modelo=row[2], ano=row[3], cor=row[4], preco=row[5], is_disponivel=bool(row[6]))
                for row in cursor.fetchall()]
    return is_locados


@route_veiculos.post('/adicionar-veiculo', status_code=status.HTTP_201_CREATED,response_model=Veiculo)
async def adicionar_veiculo(veiculo: Veiculo, cursor=Depends(get_db)):
    sql = '''INSERT INTO veiculos (marca, modelo, ano, cor, preco, is_disponivel)
VALUES (?, ?, ?, ?, ?, ?);
'''
    cursor.execute(sql,  (veiculo.marca, veiculo.modelo, veiculo.ano, veiculo.cor, veiculo.preco, veiculo.is_disponivel))    
    return veiculo


@route_veiculos.put('/atualizar-veiculo/{id_veiculo}', response_model=Veiculo, status_code=status.HTTP_200_OK)
async def atualizar_veiculo(id_veiculo: int, veiculo: Veiculo | None = None, cursor=Depends(get_db)):
    veiculo_dicionario = veiculo.dict()
    marca = veiculo_dicionario.get('marca')
    modelo = veiculo_dicionario.get('modelo')
    ano = veiculo_dicionario.get('ano')
    cor = veiculo_dicionario.get('cor')
    preco = veiculo_dicionario.get('preco')
    is_disponivel = veiculo_dicionario.get('is_disponivel')

    veiculo = Veiculo(id=id_veiculo, marca=marca, modelo=modelo, ano=ano, cor=cor, preco=preco, is_disponivel=is_disponivel)

    cursor.execute("""UPDATE veiculos
                   SET marca = ?, modelo = ?, ano = ?, cor = ?, preco = ?, is_disponivel = ?
                   WHERE id = ?""", (marca, modelo, ano, cor, preco, is_disponivel, id_veiculo))
    return veiculo


@route_veiculos.delete('/delete/{id_veiculo}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_veiculo(id_veiculo: int, cursor=Depends(get_db)):
    cursor.execute("DELETE FROM veiculos WHERE id = ?", (id_veiculo,))
    return {"message": "Veiculo de ID: {} deletado com sucesso".format(id_veiculo)}


