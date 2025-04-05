import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dto.cadastro_dto import CadastroDTO  

import pytest

def test_cadastro_dto_init():
    nickname = "test_nickname"
    name = "Test Name"
    email = "test@example.com"
    phone = "1234567890"
    birth_date = "2000-01-01"
    street = "Test Street"
    number = "123"
    zip_code = "12345"

    cadastro = CadastroDTO(nickname, name, email, phone, birth_date, street, number, zip_code)

    assert cadastro.nickname == nickname
    assert cadastro.name == name
    assert cadastro.email == email
    assert cadastro.phone == phone
    assert cadastro.birth_date == birth_date
    assert cadastro.street == street
    assert cadastro.number == number
    assert cadastro.zip_code == zip_code

def test_cadastro_dto_to_dict():
    nickname = "test_nickname"
    name = "Test Name"
    email = "test@example.com"
    phone = "1234567890"
    birth_date = "2000-01-01"
    street = "Test Street"
    number = "123"
    zip_code = "12345"

    cadastro = CadastroDTO(nickname, name, email, phone, birth_date, street, number, zip_code)
    cadastro_dict = cadastro.to_dict()

    expected_dict = {
        "nickname": nickname,
        "name": name,
        "email": email,
        "phone": phone,
        "birth_date": birth_date,
        "street": street,
        "number": number,
        "zip_code": zip_code
    }

    assert cadastro_dict == expected_dict

def test_cadastro_dto_empty_fields():
    nickname = ""
    name = ""
    email = ""
    phone = ""
    birth_date = ""
    street = ""
    number = ""
    zip_code = ""

    cadastro = CadastroDTO(nickname, name, email, phone, birth_date, street, number, zip_code)

    assert cadastro.nickname == nickname
    assert cadastro.name == name
    assert cadastro.email == email
    assert cadastro.phone == phone
    assert cadastro.birth_date == birth_date
    assert cadastro.street == street
    assert cadastro.number == number
    assert cadastro.zip_code == zip_code

def test_cadastro_dto_partial_fields():
    nickname = "partial_nickname"
    name = "Partial Name"
    email = ""
    phone = "0987654321"
    birth_date = ""
    street = "Partial Street"
    number = ""
    zip_code = "54321"

    cadastro = CadastroDTO(nickname, name, email, phone, birth_date, street, number, zip_code)

    assert cadastro.nickname == nickname
    assert cadastro.name == name
    assert cadastro.email == email
    assert cadastro.phone == phone
    assert cadastro.birth_date == birth_date
    assert cadastro.street == street
    assert cadastro.number == number
    assert cadastro.zip_code == zip_code

def test_cadastro_dto_invalid_email():
    nickname = "invalid_email_nickname"
    name = "Invalid Email Name"
    email = "invalid_email"
    phone = "1234567890"
    birth_date = "2000-01-01"
    street = "Invalid Email Street"
    number = "123"
    zip_code = "12345"

    cadastro = CadastroDTO(nickname, name, email, phone, birth_date, street, number, zip_code)

    assert cadastro.email == email 