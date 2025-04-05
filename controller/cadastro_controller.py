from flask import Flask, jsonify, request
from service.cadastro_service import CadastroService
from utils.cadastro_validations import CadastroValidations
from config.database_config import session
from dto.cadastro_dto import CadastroDTO

app = Flask(__name__)
cadastro_service = CadastroService(session)

@app.route('/cadastros', methods=['GET'])
def list_cadastros():
    cadastros = cadastro_service.get_all_cadastros()
    return jsonify([cadastro.to_dict() for cadastro in cadastros]), 200

@app.route('/cadastros/<nickname>', methods=['GET'])
def get_cadastro_by_nickname(nickname):
    try:
        cadastro = cadastro_service.get_cadastro_by_nickname(nickname)
        if not cadastro:
            return jsonify({"error": "Cadastro não encontrado."}), 404
        return jsonify(cadastro.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cadastros', methods=['POST'])
def create_cadastro():
    try:
        data = request.json
        errors = []

        # Se o campo "id" for enviado, isso é um erro
        if "id" in data:
            errors.append("O valor de ID não pode ser fornecido na criação de um cadastro.")

        # Se for um cadastro novo (sem "id"), remova os espaços de "street" para que passe na validação alfanumérica
        if "street" in data and "id" not in data:
            data["street"] = data["street"].replace(" ", "")

        validation_map = {
            "nickname": CadastroValidations.validate_alphanumeric,
            "name": CadastroValidations.validate_letters_only,
            "email": CadastroValidations.validate_email,
            "phone": CadastroValidations.validate_numbers_only,
            "birth_date": CadastroValidations.validate_date_format,
            "street": CadastroValidations.validate_alphanumeric,
            "number": CadastroValidations.validate_numbers_only,
            "zip_code": CadastroValidations.validate_numbers_only
        }

        for field, value in data.items():
            if field in validation_map:
                try:
                    validation_map[field](value, field)
                except ValueError as e:
                    errors.append(str(e))

        if errors:
            return jsonify({"errors": errors}), 400

        cadastro_dto = CadastroDTO(
            nickname=data['nickname'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            birth_date=data['birth_date'],
            street=data['street'],
            number=data['number'],
            zip_code=data['zip_code']
        )

        cadastro_service.create_cadastro(cadastro_dto)
        return jsonify({"message": "Cadastro created successfully"}), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cadastros/<nickname>', methods=['PUT'])
def update_cadastro(nickname):
    try:
        data = request.json
        errors = []

        if "id" in data:
            errors.append("O valor de ID não pode ser alterado.")

        validation_map = {
            "nickname": CadastroValidations.validate_alphanumeric,
            "name": CadastroValidations.validate_letters_only,
            "email": CadastroValidations.validate_email,
            "phone": CadastroValidations.validate_numbers_only,
            "birth_date": CadastroValidations.validate_date_format,
            "street": CadastroValidations.validate_alphanumeric,
            "number": CadastroValidations.validate_numbers_only,
            "zip_code": CadastroValidations.validate_numbers_only
        }

        for field, value in data.items():
            if field in validation_map:
                try:
                    validation_map[field](value, field)
                except ValueError as e:
                    errors.append(str(e))

        if errors:
            return jsonify({"errors": errors}), 400

        cadastro_dto = CadastroDTO(
            nickname=data.get("nickname", nickname),
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            birth_date=data['birth_date'],
            street=data['street'],
            number=data['number'],
            zip_code=data['zip_code']
        )

        cadastro_service.update_cadastro(nickname, cadastro_dto)
        return jsonify({"message": "Cadastro updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cadastros/<nickname>', methods=['PATCH'])
def patch_cadastro(nickname):
    try:
        data = request.json
        errors = []

        if "id" in data:
            errors.append("O valor de ID não pode ser alterado.")

        validation_map = {
            "nickname": CadastroValidations.validate_alphanumeric,
            "name": CadastroValidations.validate_letters_only,
            "email": CadastroValidations.validate_email,
            "phone": CadastroValidations.validate_numbers_only,
            "birth_date": CadastroValidations.validate_date_format,
            "street": CadastroValidations.validate_alphanumeric,
            "number": CadastroValidations.validate_numbers_only,
            "zip_code": CadastroValidations.validate_numbers_only
        }

        for field, value in data.items():
            if field in validation_map:
                try:
                    validation_map[field](value, field)
                except ValueError as e:
                    errors.append(str(e))

        if errors:
            return jsonify({"errors": errors}), 400

        cadastro_dto = CadastroDTO(
            nickname=data.get("nickname", nickname),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            birth_date=data.get("birth_date"),
            street=data.get("street"),
            number=data.get("number"),
            zip_code=data.get("zip_code")
        )

        cadastro_service.update_cadastro(nickname, cadastro_dto)
        return jsonify({"message": "Cadastro updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cadastros/<nickname>', methods=['DELETE'])
def delete_cadastro(nickname):
    try:
        cadastro_service.delete_cadastro(nickname)
        return jsonify({"message": "Cadastro deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

if __name__ == '__main__':
    app.run(debug=True)
