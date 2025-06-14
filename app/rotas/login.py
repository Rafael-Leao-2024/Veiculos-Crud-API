from typing import Annotated, Optional
from datetime import datetime, timedelta

from app.schema.schema_usuario import Usuario, UsuarioInDB
from app.schema.schema_token import TokenData, Token

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from werkzeug.security import check_password_hash
from jose import JWTError, jwt

from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
EXPIRE_TOKEN_ACESSO = os.getenv("EXPIRE_TOKEN_ACESSO")


router_login = APIRouter(prefix='/login', tags=["Login"])

schema_oauth2 = OAuth2PasswordBearer(tokenUrl="login/token")

# funcoes auxiliares

def pegar_usuario(username: str):
    connection = sqlite3.connect('bancosqlite.db')
    cursor = connection.cursor()
    usuario = cursor.execute('''SELECT * FROM usuarios WHERE nome = ?''', (username,)).fetchone()
    chaves = [chave[0] for chave in cursor.description]
    dicionario = dict(zip(chaves, usuario))
    return UsuarioInDB(**dicionario)

def autenticar_usuario(username:str, password:str):
    usuario = pegar_usuario(username)
    if not usuario:
        return False
    if not check_password_hash(usuario.senha, password):
        return False
    return usuario

def criar_token_acesso(dados: dict, expires_delta: Optional[timedelta]=None):
    para_encodar = dados.copy()
    if expires_delta:
        expiracao = datetime.utcnow() + expires_delta
    else:
        expiracao = timedelta(minutes=int(EXPIRE_TOKEN_ACESSO))
    para_encodar.update({"exp": expiracao})
    token_jwt = jwt.encode(para_encodar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

async def pegar_usuario_atual(token: Annotated[str, Depends(schema_oauth2)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = pegar_usuario(token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def pegar_usuario_atual_ativo(usuario_atual: Usuario = Depends(pegar_usuario_atual)):
    if usuario_atual.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario Inativo")
    return usuario_atual


@router_login.post('/token', response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = autenticar_usuario(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    acesso_token_expire = timedelta(minutes=int(EXPIRE_TOKEN_ACESSO))
    token = criar_token_acesso(
        dados={"sub": user.nome}, expires_delta=acesso_token_expire
    )
    return {"access_token": token, "token_type": "bearer"}
