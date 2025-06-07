from fastapi import FastAPI
from rotas.veiculo import route_veiculos
from rotas.user import route

app = FastAPI()

app.include_router(route)
app.include_router(route_veiculos)