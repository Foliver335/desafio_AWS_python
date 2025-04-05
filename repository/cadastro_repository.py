from entity.cadastro_entity import Cadastro


class CadastroRepository:
    def __init__(self, session):
        self.session = session

    def save(self, cadastro):
        
        self.session.add(cadastro)
        self.session.commit()

    def find_all(self):
       
        return self.session.query(Cadastro).all()

    def find_by_nickname(self, nickname):
        
        return self.session.query(Cadastro).filter_by(nickname=nickname).first()

    def update(self, cadastro):
        
        self.session.commit()

    def delete(self, cadastro):
        
        self.session.delete(cadastro)
        self.session.commit()
