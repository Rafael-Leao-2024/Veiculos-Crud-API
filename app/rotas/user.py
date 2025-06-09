from fastapi import APIRouter, status, Depends
from app.schema.modelos import Usuario, UsuarioInDB
from app.database.sessao_db import get_db
from werkzeug.security import generate_password_hash


route_user = APIRouter(prefix="/usuarios", tags=['Usuarios'])

@route_user.get('/', status_code=status.HTTP_200_OK, response_model=list[Usuario])
async def listar_usuarios(cursor=Depends(get_db)):
    linhas = cursor.execute('SELECT * FROM  usuarios').fetchall()
    usuarios = [dict(id=linha[0], nome=linha[1], email=linha[2], senha=linha[3]) for linha in linhas]
    return usuarios


@route_user.post('/create_user', status_code=status.HTTP_201_CREATED,response_model=Usuario)
async def criar_usuario(usuario: UsuarioInDB, cursor=Depends(get_db)):
    comando_sql = '''INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?); '''
    cursor.execute(comando_sql,  (usuario.nome, usuario.email, generate_password_hash(usuario.senha)))
    usuario.id = cursor.lastrowid
    return usuario


@route_user.get('/{id_usuario}', status_code=status.HTTP_200_OK, response_model=Usuario)
async def buscar_usuario(id_usuario: int, cursor=Depends(get_db)):
    usuario = cursor.execute('''SELECT * FROM usuarios WHERE id = ?''', (id_usuario,)).fetchone()
    colunas = [descricao[0] for descricao in cursor.description]
    resposta = dict(zip(colunas, usuario))
    return resposta