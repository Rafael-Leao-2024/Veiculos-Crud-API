from fastapi import APIRouter, status, Depends, HTTPException

from app.schema.schema_usuario import Usuario, UsuarioInDB, UsuarioOutput
from app.manage_database.sessao_db import get_db
from app.rotas.login import pegar_usuario_atual_ativo
from werkzeug.security import generate_password_hash



route_user = APIRouter(prefix="/usuarios", tags=['Usuarios'], dependencies=[Depends(pegar_usuario_atual_ativo)])

@route_user.get('/', status_code=status.HTTP_200_OK, response_model=list[UsuarioOutput])
async def listar_usuarios(cursor=Depends(get_db)):
    # if not usuario:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Unauthorized")
    linhas = cursor.execute('SELECT * FROM  usuarios').fetchall()
    usuarios = [dict(id=linha[0], nome=linha[1], email=linha[2], senha=linha[3]) for linha in linhas]
    return usuarios


@route_user.get('/{id_usuario}', status_code=status.HTTP_200_OK, response_model=UsuarioOutput)
async def buscar_usuario(id_usuario: int, cursor=Depends(get_db)):
    usuario = cursor.execute('''SELECT * FROM usuarios WHERE id = ?''', (id_usuario,)).fetchone()
    if not usuario:
        raise HTTPException(status_code=404, detail="user not found")
    colunas = [descricao[0] for descricao in cursor.description]
    resposta = dict(zip(colunas, usuario))
    return resposta


@route_user.post('/create-user', status_code=status.HTTP_201_CREATED,response_model=UsuarioOutput)
async def criar_usuario(usuario: Usuario, cursor=Depends(get_db)):
    if not usuario.nome or not usuario.email or not usuario.senha:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Os Campos nao foram preenchidos")
    dicionario = usuario.model_dump(exclude_unset=True)
    dicionario.update({"id": 1})
    usuario = UsuarioInDB(**dicionario)
    comando_sql = '''INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?); '''
    cursor.execute(comando_sql,  (usuario.nome, usuario.email, generate_password_hash(usuario.senha)))
    usuario.id = cursor.lastrowid
    print(usuario)
    return usuario



