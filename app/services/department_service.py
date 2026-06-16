from app.daos.department_dao import DepartmentDAO
from app.interfaces.service_interface import IService
from app.services.log_service import LogService


class DepartmentService(IService):
    def __init__(self):
        self.dao = DepartmentDAO()
        self.log_service = LogService()

    def list(self):
        return self.dao.find_all()

    def get(self, id):
        return self.dao.find_by_id(id)

    def store(self, data):
        department = self.dao.create(
            {
                "name": (data.get("name") or "").strip(),
                "description": (data.get("description") or "").strip() or None,
            }
        )
        self.log_service.save_log(
            "CREATE", "cadastro", "departments", department.id, department.to_dict()
        )
        return department

    def update(self, id, data):
        department = self.dao.update(
            id,
            {
                "name": (data.get("name") or "").strip(),
                "description": (data.get("description") or "").strip() or None,
            },
        )
        if department:
            self.log_service.save_log(
                "UPDATE", "alteracao", "departments", department.id, department.to_dict()
            )
        return department

    def delete(self, id):
        deleted = self.dao.delete(id)
        if deleted:
            self.log_service.save_log("DELETE", "exclusao", "departments", id)
        return deleted
