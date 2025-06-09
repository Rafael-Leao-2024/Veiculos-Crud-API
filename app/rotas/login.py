from typing import Annotated

from app.schema.modelos import Usuario
from app.database.sessao_db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router_login = APIRouter(prefix='/login', tags=["Login"])

@router_login.post('/', response_model=Usuario)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], cursor=Depends(get_db)):
    usuario = cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (form_data.username, )).fetchone()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario nao Encontrado")
    user_dict = dict(zip([coluna[0] for coluna in cursor.description], usuario))
    return user_dict