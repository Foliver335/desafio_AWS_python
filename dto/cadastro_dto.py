from typing import Dict, Any

class CadastroDTO:
    def __init__(self, nickname: str, name: str, email: str, phone: str, birth_date: str, street: str, number: str, zip_code: str) -> None:
        self.nickname = nickname
        self.name = name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.street = street
        self.number = number
        self.zip_code = zip_code
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nickname": self.nickname,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "birth_date": self.birth_date,
            "street": self.street,
            "number": self.number,
            "zip_code": self.zip_code
        }
