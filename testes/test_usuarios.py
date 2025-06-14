from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.environ.get("TOKEN")

headers = {"Authorization": f"Bearer {TOKEN}"}


cliente = TestClient(app)


def test_criar_usuarios():
    dados = {
        "nome":"Rafael", 
        "email": "@rafael",
        "disabled":True,
        "senha": "5811"     
        }
    
    response = cliente.post('/usuarios/create-user', json=dados, headers=headers)
    print(response.content)
    assert response.status_code == 201
    assert "id" in  response.json()
    assert response.json().get("nome") == dados.get("nome")


def test_criar_usuarios_invalido_campos():
    dados = {
        "nome":"Rafael", 
        "email": "@rafael",
        "disabled":True,    
        }
    
    response = cliente.post('/usuarios/create-user', json=dados, headers=headers)
    print(response.content)
    assert response.status_code == 422
    assert response.json().get("nome") is None


def test_campos_nao_preenchidos():
    dados = {
        "nome":"", 
        "email": "",
        "senha":""  
        }
    response = cliente.post('/usuarios/create-user', json=dados, headers=headers)
    assert response.status_code == 400
    assert response.json().get('detail') == "Os Campos nao foram preenchidos"


def test_pegar_todos_usuarios():
    response = cliente.get('/usuarios/', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 0
    

def test_buscar_id_user_invalido():
    resposta = cliente.get('/usuarios/999999999999', headers=headers)
    assert resposta.status_code == 404
    assert resposta.request.method == "GET"


def test_buscar_id_user_valido():
    resposta = cliente.get('/usuarios/1', headers=headers)
    assert resposta.status_code == 200
    assert "nome" in resposta.json()
    assert resposta.json().get("id") == 1

