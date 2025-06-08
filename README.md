# 🚗 Veículos CRUD API

Uma API simples para gerenciamento de veículos, construída com **FastAPI**.  
**Recursos**: CRUD completo, documentação automática e banco de dados em memória.

🔗 **Repositório**: [github.com/Rafael-Leao-2024/veiculos-crud-api](https://github.com/Rafael-Leao-2024/veiculos-crud-api)

---

## 📌 **Funcionalidades**

- **Listar todos os veículos** (`GET /veiculos/`)
- **Buscar veículo por ID** (`GET /veiculos/{id_veiculo}`)
- **Adicionar novo veículo** (`POST /veiculos/adicionar-veiculo`)
- **Atualizar veículo** (`PUT /veiculos/atualizar-veiculo/{id_veiculo}`)
- **Deletar veículo** (`DELETE /veiculos/delete/{id_veiculo}`)

---

## ⚙️ **Tecnologias**

- **Python 3.12.6**
- **FastAPI** (Framework web)
- **Pydantic** (Validação de dados)
- **Swagger UI** (Documentação interativa em `/docs`)

---

## 🚀 **Como Executar**

### **Pré-requisitos**

- Python 3.12.6 instalado
- Pip (gerenciador de pacotes)

### **Passos**

1. Clone o repositório:

   ```sh
   git clone https://github.com/Rafael-Leao-2024/veiculos-crud-api.git
   cd veiculos-crud-api
   ```

2. Instale as dependências:

   ```
   pip install -r requiriments.txt
   ```

3. Execute o servidor:

   ```
    uvicorn app.main:app --reload
   ```

4. Acesse a documentação interativa:

🔹 Swagger UI: http://127.0.0.1:8000/docs
🔹 Redoc: http://127.0.0.1:8000/redoc
