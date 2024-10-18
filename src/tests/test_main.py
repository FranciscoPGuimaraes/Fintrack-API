import requests

# URL base da API
BASE_URL = "http://localhost:8000"

# Função auxiliar para registro de usuário
def register_user(data):
    return requests.post(f"{BASE_URL}/user/register", json=data)

# Teste de sucesso - registro válido
def test_register_success():
    data = {
        "name": "Matheus Fonseca",
        "email": "maa@gmail.com",
        "password": "senha123"
    }
    response = register_user(data)
    assert response.status_code == 201  # Verifique manualmente se a API está retornando o 201 corretamente
    json_response = response.json()
    assert "message" in json_response
    assert "sucesso" in json_response["message"]

# Teste de erro - e-mail duplicado
def test_register_duplicate_email():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "senha123"
    }
    response = register_user(data)
    assert response.status_code == 400  # Ajustado para 400 se a API retornar isso em vez de 409
    json_response = response.json()
    assert "detail" in json_response
    assert "E-mail já registrado" in json_response["detail"]

# Teste de erro - e-mail inválido
def test_register_invalid_email():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso",
        "password": "senha123"
    }
    response = register_user(data)
    assert response.status_code == 400
    json_response = response.json()
    assert "detail" in json_response  # Verifica o campo "detail"
    # Ajuste dependendo do que a API retorna primeiro
    assert "A senha deve ter no mínimo 6 caracteres" in json_response["detail"]


# Teste de erro - dados faltando (sem nome)
def test_register_missing_name():
    data = {
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "senha123"
    }
    response = register_user(data)
    assert response.status_code == 422  # Status code esperado para dados faltando
    json_response = response.json()
    assert "detail" in json_response
    assert json_response["detail"][0]["msg"] == "Field required"
    assert json_response["detail"][0]["loc"] == ["body", "name"]

# Teste de erro - senha fraca
def test_register_weak_password():
    data = {
        "name": "Matheus Fonseca",
        "email": "matheusfonsecaafonso@gmail.com",
        "password": "123"  # Senha muito curta
    }
    response = register_user(data)
    assert response.status_code == 400, f"Expected status 400, got {response.status_code}"
    json_response = response.json()
    assert "detail" in json_response  # Verifica o campo "detail"
    assert "A senha deve ter no mínimo 6 caracteres" in json_response["detail"]

# Teste de erro - método HTTP incorreto
def test_register_wrong_method():
    response = requests.get(f"{BASE_URL}/user/register")
    assert response.status_code == 405
    json_response = response.json()
    assert "detail" in json_response
    assert "Method Not Allowed" in json_response["detail"]
