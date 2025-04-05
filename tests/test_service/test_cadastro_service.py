import pytest
from unittest.mock import MagicMock
from datetime import datetime
from service.cadastro_service import CadastroService
from entity.cadastro_entity import Cadastro


class MockCadastroDTO:
    def __init__(self, nickname, name, email, phone, birth_date, street, number, zip_code):
        self.nickname = nickname
        self.name = name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.street = street
        self.number = number
        self.zip_code = zip_code


# ✅ Função auxiliar para retornar um Cadastro válido
def fake_cadastro_obj():
    return Cadastro(
        nickname="johndoe",
        name="John Doe",
        email="john@example.com",
        phone="123456789",
        birth_date=datetime.strptime("1990-01-01", "%Y-%m-%d").date(),
        street="Main St",
        number="100",
        zip_code="12345-678"
    )


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    return repo


@pytest.fixture
def cadastro_service(mock_repository):
    service = CadastroService.__new__(CadastroService)
    service.repository = mock_repository
    return service


def test_create_cadastro_success(cadastro_service, mock_repository):
    dto = MockCadastroDTO("johndoe", "John Doe", "john@example.com", "123456789", "1990-01-01", "Main St", "100", "12345-678")
    mock_repository.find_by_nickname.return_value = None

    cadastro_service.create_cadastro(dto)

    assert mock_repository.save.called
    saved_cadastro = mock_repository.save.call_args[0][0]
    assert saved_cadastro.nickname == "johndoe"
    assert saved_cadastro.birth_date == datetime.strptime("1990-01-01", "%Y-%m-%d").date()


def test_create_cadastro_duplicate_nickname(cadastro_service, mock_repository):
    dto = MockCadastroDTO("johndoe", "John", "john@example.com", "123", "1990-01-01", "Street", "1", "00000")
    mock_repository.find_by_nickname.return_value = fake_cadastro_obj()

    with pytest.raises(ValueError, match="Cadastro com este nickname já existe."):
        cadastro_service.create_cadastro(dto)


def test_get_all_cadastros(cadastro_service, mock_repository):
    mock_repository.find_all.return_value = ["cadastro1", "cadastro2"]

    result = cadastro_service.get_all_cadastros()

    assert result == ["cadastro1", "cadastro2"]
    assert mock_repository.find_all.called


def test_get_cadastro_by_nickname_found(cadastro_service, mock_repository):
    cadastro = fake_cadastro_obj()
    mock_repository.find_by_nickname.return_value = cadastro

    result = cadastro_service.get_cadastro_by_nickname("nickname")

    assert result == cadastro
    assert mock_repository.find_by_nickname.called


def test_get_cadastro_by_nickname_not_found(cadastro_service, mock_repository):
    mock_repository.find_by_nickname.return_value = None

    with pytest.raises(ValueError, match="Cadastro não encontrado."):
        cadastro_service.get_cadastro_by_nickname("nickname")


def test_update_cadastro_success(cadastro_service, mock_repository):
    existing_cadastro = fake_cadastro_obj()
    mock_repository.find_by_nickname.side_effect = [existing_cadastro, None]

    dto = MockCadastroDTO("newnick", "New Name", "new@example.com", "987654321", "1980-12-12", "New St", "200", "98765-432")

    cadastro_service.update_cadastro("oldnick", dto)

    assert mock_repository.update.called
    updated = mock_repository.update.call_args[0][0]
    assert updated.nickname == "newnick"
    assert updated.name == "New Name"


def test_update_cadastro_not_found(cadastro_service, mock_repository):
    mock_repository.find_by_nickname.return_value = None

    dto = MockCadastroDTO("nick", "Name", "email", "phone", "2000-01-01", "Street", "1", "00000")

    with pytest.raises(ValueError, match="Cadastro não encontrado."):
        cadastro_service.update_cadastro("nonexistent", dto)


def test_update_cadastro_nickname_conflict(cadastro_service, mock_repository):
    cadastro = fake_cadastro_obj()
    mock_repository.find_by_nickname.side_effect = [cadastro, fake_cadastro_obj()]  # segundo é conflito

    dto = MockCadastroDTO("newnick", "Name", "email", "phone", "2000-01-01", "Street", "1", "00000")

    with pytest.raises(ValueError, match="O nickname já está em uso por outro cadastro."):
        cadastro_service.update_cadastro("oldnick", dto)


def test_delete_cadastro_success(cadastro_service, mock_repository):
    cadastro = fake_cadastro_obj()
    mock_repository.find_by_nickname.return_value = cadastro

    cadastro_service.delete_cadastro("nickname")

    assert mock_repository.delete.called
    assert mock_repository.delete.call_args[0][0] == cadastro


def test_delete_cadastro_not_found(cadastro_service, mock_repository):
    mock_repository.find_by_nickname.return_value = None

    with pytest.raises(ValueError, match="Cadastro não encontrado."):
        cadastro_service.delete_cadastro("nickname")
