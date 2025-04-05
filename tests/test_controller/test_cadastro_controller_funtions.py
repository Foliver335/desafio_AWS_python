import sys
import os
from unittest.mock import MagicMock
import pytest

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from controller import cadastro_controller

app = cadastro_controller.app
cadastro_service = cadastro_controller.cadastro_service

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

# Teste para GET /cadastros
def test_list_cadastros(client, monkeypatch):
    # Configura um mock para o método get_all_cadastros do serviço
    mock_service = MagicMock()
    mock_service.get_all_cadastros.return_value = [
        MagicMock(to_dict=lambda: {"nickname": "user1"}),
        MagicMock(to_dict=lambda: {"nickname": "user2"})
    ]
    monkeypatch.setattr(cadastro_controller, 'cadastro_service', mock_service)
    
    response = client.get('/cadastros')
    
    assert response.status_code == 200
    assert response.json == [{"nickname": "user1"}, {"nickname": "user2"}]

# Teste para GET /cadastros/<nickname> (caso encontrado)
def test_get_cadastro_by_nickname_found(client, monkeypatch):
    mock_service = MagicMock()
    mock_service.get_cadastro_by_nickname.return_value = MagicMock(to_dict=lambda: {"nickname": "user1"})
    monkeypatch.setattr(cadastro_controller, 'cadastro_service', mock_service)
    
    response = client.get('/cadastros/user1')
    
    assert response.status_code == 200
    assert response.json == {"nickname": "user1"}

# Teste para GET /cadastros/<nickname> (caso não encontrado)
def test_get_cadastro_by_nickname_not_found(client, monkeypatch):
    mock_service = MagicMock()
    mock_service.get_cadastro_by_nickname.return_value = None
    monkeypatch.setattr(cadastro_controller, 'cadastro_service', mock_service)
    
    response = client.get('/cadastros/nonexistent')
    
    assert response.status_code == 404
    assert response.json == {"error": "Cadastro não encontrado."}

# Teste para POST /cadastros (criação bem-sucedida)
def test_create_cadastro_success(client, monkeypatch):
    # Dados válidos para criação (note que "street" contém espaço,
    # mas o controller deve removê-lo para cadastro novo)
    new_cadastro = {
        "nickname": "user1",
        "name": "User One",
        "email": "user1@example.com",
        "phone": "1234567890",
        "birth_date": "2000-01-01",
        "street": "Main St",
        "number": "123",
        "zip_code": "12345"
    }
    # Substitui a implementação real para evitar efeitos colaterais
    monkeypatch.setattr(cadastro_service, "create_cadastro", lambda cadastro_dto: None)
    
    response = client.post('/cadastros', json=new_cadastro)
    
    # Espera-se que o controller remova os espaços de "street" e crie o cadastro
    assert response.status_code == 201
    assert response.json == {"message": "Cadastro created successfully"}

# Teste para POST /cadastros (criação com erros)
def test_create_cadastro_with_errors(client, monkeypatch):
    # Dados inválidos: contém "id", email inválido e "street" com espaço
    new_cadastro = {
        "id": 1,
        "nickname": "user1",
        "name": "User One",
        "email": "invalid-email",
        "phone": "1234567890",
        "birth_date": "2000-01-01",
        "street": "Main St",  # Como "id" está presente, o controller NÃO remove espaços
        "number": "123",
        "zip_code": "12345"
    }
    monkeypatch.setattr(cadastro_service, "create_cadastro", lambda cadastro_dto: None)
    
    response = client.post('/cadastros', json=new_cadastro)
    
    assert response.status_code == 400
    errors = response.json.get("errors", [])
    # Verifica os erros esperados
    assert "O valor de ID não pode ser fornecido na criação de um cadastro." in errors
    assert "O campo 'email' deve conter um e-mail válido." in errors
    assert "O campo 'street' deve conter apenas caracteres alfanuméricos." in errors

# Teste para PUT /cadastros/<nickname> (atualização bem-sucedida)
def test_update_cadastro_success(client, monkeypatch):
    updated_data = {
        "name": "User One Updated",
        "email": "user1updated@example.com",
        "phone": "0987654321",
        "birth_date": "2000-01-01",
        "street": "MainSt",  # Valor já válido (sem espaço)
        "number": "123",
        "zip_code": "12345"
    }
    monkeypatch.setattr(cadastro_service, "update_cadastro", lambda nickname, cadastro_dto: None)
    
    response = client.put('/cadastros/user1', json=updated_data)
    
    assert response.status_code == 200
    assert response.json == {"message": "Cadastro updated successfully"}

# Teste para PATCH /cadastros/<nickname> (atualização parcial bem-sucedida)
def test_patch_cadastro_success(client, monkeypatch):
    patch_data = {
        "email": "user1patched@example.com"
    }
    monkeypatch.setattr(cadastro_service, "update_cadastro", lambda nickname, cadastro_dto: None)
    
    response = client.patch('/cadastros/user1', json=patch_data)
    
    assert response.status_code == 200
    assert response.json == {"message": "Cadastro updated successfully"}

# Teste para DELETE /cadastros/<nickname>
def test_delete_cadastro_success(client, monkeypatch):
    monkeypatch.setattr(cadastro_service, "delete_cadastro", lambda nickname: None)
    
    response = client.delete('/cadastros/user1')
    
    assert response.status_code == 200
    assert response.json == {"message": "Cadastro deleted successfully"}
