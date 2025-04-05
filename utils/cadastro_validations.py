class CadastroValidations:
    @staticmethod
    def validate_alphanumeric(value, field_name):
        if not value or not value.isalnum():
            raise ValueError(f"O campo '{field_name}' deve conter apenas caracteres alfanuméricos.")

    @staticmethod
    def validate_letters_only(value, field_name):
        if not value or not all(char.isalpha() or char.isspace() for char in value):
            raise ValueError(f"O campo '{field_name}' deve conter apenas letras e espaços.")


    @staticmethod
    def validate_email(value, field_name):
        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValueError(f"O campo '{field_name}' deve conter um e-mail válido.")

    @staticmethod
    def validate_numbers_only(value, field_name):
        if not value.isdigit():
            raise ValueError(f"O campo '{field_name}' deve conter apenas números.")

    
    def validate_date_format(value, field_name="birth_date"):
        from datetime import datetime
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"O campo '{field_name}' deve estar no formato YYYY-MM-DD.")


    @staticmethod
    def validate_address(address):
       
        CadastroValidations.validate_alphanumeric(address.get("street"), "street")
        CadastroValidations.validate_numbers_only(address.get("number"), "number")
        CadastroValidations.validate_numbers_only(address.get("zip_code"), "zip_code")
