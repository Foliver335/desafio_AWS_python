from repository.cadastro_repository import CadastroRepository
from entity.cadastro_entity import Cadastro
from datetime import datetime


class CadastroService:
    def __init__(self, session):
        self.repository = CadastroRepository(session)

    def create_cadastro(self, cadastro_dto):
        existing_cadastro = self.repository.find_by_nickname(cadastro_dto.nickname)
        if existing_cadastro:
            raise ValueError("Cadastro com este nickname já existe.")
        
        new_cadastro = Cadastro(
            nickname=cadastro_dto.nickname,
            name=cadastro_dto.name,
            email=cadastro_dto.email,
            phone=cadastro_dto.phone,
            birth_date=datetime.strptime(cadastro_dto.birth_date, '%Y-%m-%d').date(),
            street=cadastro_dto.street,
            number=cadastro_dto.number,
            zip_code=cadastro_dto.zip_code
        )
        self.repository.save(new_cadastro)

    def get_all_cadastros(self):
        
        return self.repository.find_all()
    
    def get_cadastro_by_nickname(self, nickname):
    
        cadastro = self.repository.find_by_nickname(nickname)
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")
        return cadastro

    def update_cadastro(self, old_nickname, cadastro_dto):
        cadastro = self.repository.find_by_nickname(old_nickname)
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")

        if cadastro_dto.nickname and cadastro_dto.nickname != old_nickname:
            existing_cadastro = self.repository.find_by_nickname(cadastro_dto.nickname)
            print(f"Encontrado: {existing_cadastro}")
            if existing_cadastro:
                raise ValueError("O nickname já está em uso por outro cadastro.")

        fields_to_update = {
            "nickname": cadastro_dto.nickname if cadastro_dto.nickname else old_nickname,
            "name": cadastro_dto.name,
            "email": cadastro_dto.email,
            "phone": cadastro_dto.phone,
            "birth_date": datetime.strptime(cadastro_dto.birth_date, '%Y-%m-%d').date() if cadastro_dto.birth_date else None,
            "street": cadastro_dto.street,
            "number": cadastro_dto.number,
            "zip_code": cadastro_dto.zip_code,
        }
        

        for attr, value in fields_to_update.items():
            if value is not None:
                setattr(cadastro, attr, value)
            

        self.repository.update(cadastro)

    def delete_cadastro(self, nickname):
       
        cadastro = self.repository.find_by_nickname(nickname)
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")
        
        self.repository.delete(cadastro)
