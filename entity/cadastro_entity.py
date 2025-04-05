from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cadastro(Base):
    __tablename__ = 'cadastros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, unique=True, nullable=False)  # Identificador único
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    street = Column(String, nullable=False)
    number = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)

    def __init__(self, nickname, name, email, phone, birth_date, street, number, zip_code):
        self.nickname = nickname
        self.name = name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.street = street
        self.number = number
        self.zip_code = zip_code

    def to_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "birth_date": self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None,  # Formata a data
            "street": self.street,
            "number": self.number,
            "zip_code": self.zip_code
        }
