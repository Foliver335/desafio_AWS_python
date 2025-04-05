import sys
import os
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import unittest
import uuid

# Adiciona a raiz do projeto ao sys.path para que o Python encontre a pasta 'cadastro_entity'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Agora importa a entidade 'Cadastro' e 'Base' do arquivo correto
from entity.cadastro_entity import Base, Cadastro

class TestCadastroEntity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Cria um banco de dados SQLite na memória
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        # Limpa os dados de cada tabela após o teste
        self.session.query(Cadastro).delete()
        self.session.commit()
        self.session.close()

    def test_create_cadastro(self):
        # Cria um cadastro com um 'nickname' único usando uuid
        cadastro = Cadastro(
            nickname=str(uuid.uuid4()),  # Garante que o nickname seja único
            name="Test User",
            email="testuser@example.com",
            phone="1234567890",
            birth_date=date(1990, 1, 1),
            street="Test Street",
            number="123",
            zip_code="12345"
        )
        self.session.add(cadastro)
        self.session.commit()

        result = self.session.query(Cadastro).filter_by(nickname=cadastro.nickname).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.nickname, cadastro.nickname)
        self.assertEqual(result.name, "Test User")
        self.assertEqual(result.email, "testuser@example.com")
        self.assertEqual(result.phone, "1234567890")
        self.assertEqual(result.birth_date, date(1990, 1, 1))
        self.assertEqual(result.street, "Test Street")
        self.assertEqual(result.number, "123")
        self.assertEqual(result.zip_code, "12345")

    def test_to_dict(self):
        # Cria um cadastro com um 'nickname' único usando uuid
        cadastro = Cadastro(
            nickname=str(uuid.uuid4()),  # Garante que o nickname seja único
            name="Test User",
            email="testuser@example.com",
            phone="1234567890",
            birth_date=date(1990, 1, 1),
            street="Test Street",
            number="123",
            zip_code="12345"
        )
        self.session.add(cadastro)
        self.session.commit()

        result = self.session.query(Cadastro).filter_by(nickname=cadastro.nickname).first()
        expected_dict = {
            "id": result.id,
            "nickname": result.nickname,
            "name": "Test User",
            "email": "testuser@example.com",
            "phone": "1234567890",
            "birth_date": "1990-01-01",
            "street": "Test Street",
            "number": "123",
            "zip_code": "12345"
        }
        self.assertEqual(result.to_dict(), expected_dict)

if __name__ == '__main__':
    unittest.main()
