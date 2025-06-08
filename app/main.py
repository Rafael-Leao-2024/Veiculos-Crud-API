from fastapi import FastAPI
from app.rotas.veiculo import route_veiculos
from app.rotas.user import route_user

app = FastAPI()


app.include_router(route_user)
app.include_router(route_veiculos)