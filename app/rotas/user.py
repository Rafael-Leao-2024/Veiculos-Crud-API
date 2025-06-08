from fastapi import APIRouter, status
from app.schema.modelos import UserPublic

users_db = []

route_user = APIRouter(prefix="/usuarios", tags=['Usuarios'])

@route_user.get('/', status_code=status.HTTP_200_OK, response_model=list[UserPublic])
async def listar_usuarios():
    return users_db


@route_user.get('/{id_usuario}', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def buscar_usuario(id_usuario: int):
    return users_db[id_usuario - 1]