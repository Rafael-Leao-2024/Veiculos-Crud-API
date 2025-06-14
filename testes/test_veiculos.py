from fastapi.testclient import TestClient
from app.main import app  # Importe sua aplicação FastAPI

client = TestClient(app)

def test_buscar_veiculo_id_valido():
    response = client.get("/veiculos/1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "marca" in response.json()  # Adapte para seus campos

def test_buscar_veiculo_id_inexistente():
    response = client.get("/veiculos/999999")  # ID que não existe
    assert response.status_code == 404
    assert response.json() == {"detail": "Veículo não encontrado"}


def test_buscar_veiculo_id_nao_numerico():
    response = client.get("/veiculos/abc")
    assert response.status_code == 422  # Unprocessable Entity (FastAPI valida o tipo)