from fastapi import APIRouter, status
from database.banco_fake import users_db
from schema.modelos import UserPublic

route = APIRouter(prefix="/usuarios", tags=['Usuarios'])

@route.get('/', status_code=status.HTTP_200_OK, response_model=list[UserPublic])
async def listar_usuarios():
    return users_db