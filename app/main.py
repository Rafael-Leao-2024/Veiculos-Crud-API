from fastapi import FastAPI
from app.rotas.login import router_login
from app.rotas.veiculo import route_veiculos
from app.rotas.user import route_user

app = FastAPI()

@app.get('/')
async def home_api():
    return {"mesage": "Hello World!"}

app.include_router(router_login)
app.include_router(route_user)
app.include_router(route_veiculos)

