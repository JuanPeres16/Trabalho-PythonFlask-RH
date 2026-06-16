import json

from flask import flash, jsonify, redirect, request


ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def init_validation_middleware(app):
    @app.before_request
    def validate_private_forms():
        if request.method not in {"POST", "PUT"}:
            return None

        path = request.path.rstrip("/")
        errors = []

        if _matches_entity_write(path, "employees"):
            data = request.get_json(silent=True) if request.is_json else request.form
            errors = validate_employee_form(data or {}, request.files.get("photo"))
        elif _matches_entity_write(path, "departments"):
            errors = validate_department_form(_request_data())
        elif _matches_entity_write(path, "positions"):
            errors = validate_position_form(_request_data())
        elif _matches_entity_write(path, "skills"):
            errors = validate_skill_form(_request_data())

        if not errors:
            return None

        if request.method == "PUT" or request.is_json or request.path.startswith("/api"):
            return jsonify({"errors": errors}), 422

        for error in errors:
            flash(error, "error")
        return redirect(request.referrer or "/dashboard")


def validate_department_form(data):
    errors = []
    if not (data.get("name") or "").strip():
        errors.append("Informe o nome do departamento.")
    return errors


def validate_position_form(data):
    errors = []
    if not data.get("department_id"):
        errors.append("Selecione um departamento.")
    if not (data.get("name") or "").strip():
        errors.append("Informe o nome do cargo.")
    return errors


def validate_skill_form(data):
    errors = []
    if not (data.get("name") or "").strip():
        errors.append("Informe o nome da habilidade.")
    return errors


def validate_employee_form(data, file_storage=None):
    errors = []
    required = {
        "position_id": "Selecione um cargo.",
        "name": "Informe o nome do colaborador.",
        "email": "Informe o e-mail.",
        "document": "Informe o documento.",
        "admission_date": "Informe a data de admissao.",
        "status": "Selecione o status.",
    }

    for field, message in required.items():
        if not (data.get(field) or "").strip():
            errors.append(message)

    if data.get("email") and "@" not in data.get("email"):
        errors.append("Informe um e-mail valido.")

    errors.extend(validate_image_file(file_storage))
    return errors


def validate_json_file(file_storage):
    errors = []
    if not file_storage or not file_storage.filename:
        return ["Selecione um arquivo JSON."]
    if not file_storage.filename.lower().endswith(".json"):
        return ["O arquivo precisa ter extensao .json."]
    try:
        position = file_storage.stream.tell()
        json.load(file_storage.stream)
        file_storage.stream.seek(position)
    except Exception:
        errors.append("O arquivo JSON esta invalido.")
    return errors


def validate_image_file(file_storage):
    if not file_storage or not file_storage.filename:
        return []
    filename = file_storage.filename.lower()
    extension = filename.rsplit(".", 1)[-1] if "." in filename else ""
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return ["A imagem deve ser png, jpg, jpeg ou webp."]
    return []


def _request_data():
    return request.get_json(silent=True) if request.is_json else request.form


def _matches_entity_write(path, entity):
    if path == f"/{entity}":
        return True
    if path.endswith("/delete"):
        return False
    if path.startswith(f"/{entity}/") and path.endswith("/update"):
        return True
    if request.method == "PUT" and path.startswith(f"/{entity}/"):
        return True
    return False
