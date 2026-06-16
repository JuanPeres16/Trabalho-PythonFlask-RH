import os
import uuid
from datetime import date, datetime

from flask import current_app
from werkzeug.utils import secure_filename

from app.daos.employee_dao import EmployeeDAO
from app.interfaces.service_interface import IService
from app.services.log_service import LogService


class EmployeeService(IService):
    def __init__(self):
        self.dao = EmployeeDAO()
        self.log_service = LogService()

    def list(self, filters=None):
        return self.dao.search(self._prepare_filters(filters or {}))

    def get(self, id):
        return self.dao.find_by_id(id)

    def store(self, data):
        payload = self._payload(data)
        employee = self.dao.create(payload)
        self.log_service.save_log(
            "CREATE", "cadastro", "employees", employee.id, employee.to_dict()
        )
        return employee

    def update(self, id, data):
        employee = self.get(id)
        if not employee:
            return None

        payload = self._payload(data, current_photo=employee.photo_path)
        employee = self.dao.update(id, payload)
        self.log_service.save_log(
            "UPDATE", "alteracao", "employees", employee.id, employee.to_dict()
        )
        return employee

    def delete(self, id):
        deleted = self.dao.delete(id)
        if deleted:
            self.log_service.save_log("DELETE", "exclusao", "employees", id)
        return deleted

    def total(self):
        return len(self.dao.find_all())

    def total_by_status(self, status):
        return self.dao.count_by_status(status)

    def _payload(self, data, current_photo=None):
        form = data.get("form", data) if isinstance(data, dict) else data
        photo_file = data.get("photo_file") if isinstance(data, dict) else None
        photo_path = self._save_photo(photo_file) or current_photo

        payload = {
            "position_id": int(self._get(form, "position_id")),
            "name": self._get(form, "name").strip(),
            "email": self._get(form, "email").strip().lower(),
            "phone": self._get(form, "phone").strip() or None,
            "document": self._get(form, "document").strip(),
            "birth_date": self._parse_date(self._get(form, "birth_date")),
            "admission_date": self._parse_date(self._get(form, "admission_date")),
            "status": self._get(form, "status", "ativo") or "ativo",
            "skill_ids": self._getlist(form, "skill_ids"),
        }

        if photo_path:
            payload["photo_path"] = photo_path

        return payload

    def _prepare_filters(self, filters):
        return {
            "name": self._get(filters, "name"),
            "department_id": self._get(filters, "department_id"),
            "position_id": self._get(filters, "position_id"),
            "status": self._get(filters, "status"),
            "admission_start": self._parse_date(self._get(filters, "admission_start")),
            "admission_end": self._parse_date(self._get(filters, "admission_end")),
        }

    def _save_photo(self, photo_file):
        if not photo_file or not photo_file.filename:
            return None

        filename = secure_filename(photo_file.filename)
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if extension not in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            raise ValueError("Formato de imagem invalido.")

        final_name = f"{uuid.uuid4().hex}.{extension}"
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)
        photo_file.save(os.path.join(upload_folder, final_name))
        return f"uploads/employees/{final_name}"

    def _parse_date(self, value):
        if not value:
            return None
        if isinstance(value, date):
            return value
        return datetime.strptime(str(value), "%Y-%m-%d").date()

    def _get(self, data, key, default=""):
        return data.get(key, default) if data is not None else default

    def _getlist(self, data, key):
        if hasattr(data, "getlist"):
            return data.getlist(key)
        value = data.get(key, []) if data is not None else []
        return value if isinstance(value, list) else [value]
