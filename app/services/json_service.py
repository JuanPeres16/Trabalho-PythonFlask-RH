import json

from app.daos.department_dao import DepartmentDAO
from app.daos.position_dao import PositionDAO
from app.daos.skill_dao import SkillDAO
from app.models.employee import Employee
from app.services.department_service import DepartmentService
from app.services.employee_service import EmployeeService
from app.services.log_service import LogService
from app.services.position_service import PositionService
from app.services.skill_service import SkillService


class JsonService:
    def __init__(self):
        self.log_service = LogService()
        self.employee_service = EmployeeService()
        self.department_service = DepartmentService()
        self.position_service = PositionService()
        self.skill_service = SkillService()

    def export_entity(self, entity):
        data = [item.to_dict() for item in self._all(entity)]
        self.log_service.save_log(
            "EXPORT_JSON",
            "exportacao_json",
            entity,
            None,
            {"total": len(data)},
        )
        return json.dumps(data, ensure_ascii=False, indent=2, default=str)

    def import_entity(self, entity, file_storage):
        raw = json.load(file_storage.stream)
        records = raw.get("items", raw) if isinstance(raw, dict) else raw
        if not isinstance(records, list):
            raise ValueError("O JSON deve conter uma lista de registros.")

        imported = 0
        for record in records:
            if not isinstance(record, dict):
                continue
            self._store(entity, record)
            imported += 1

        self.log_service.save_log(
            "IMPORT_JSON",
            "importacao_json",
            entity,
            None,
            {"total_importado": imported},
        )
        return imported

    def _all(self, entity):
        if entity == "employees":
            return Employee.query.order_by(Employee.name.asc()).all()
        if entity == "departments":
            return DepartmentDAO().find_all()
        if entity == "positions":
            return PositionDAO().find_all()
        if entity == "skills":
            return SkillDAO().find_all()
        raise ValueError("Entidade nao permitida para exportacao.")

    def _store(self, entity, record):
        if entity == "employees":
            data = dict(record)
            if not data.get("position_id"):
                raise ValueError("Colaborador importado precisa de position_id.")
            self.employee_service.store(data)
            return
        if entity == "departments":
            self.department_service.store(record)
            return
        if entity == "positions":
            self.position_service.store(record)
            return
        if entity == "skills":
            self.skill_service.store(record)
            return
        raise ValueError("Entidade nao permitida para importacao.")
