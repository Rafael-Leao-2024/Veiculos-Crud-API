from fastapi import FastAPI
from rotas.veiculo import route_veiculos
from rotas.user import route_user

app = FastAPI()


app.include_router(route_user)
app.include_router(route_veiculos)