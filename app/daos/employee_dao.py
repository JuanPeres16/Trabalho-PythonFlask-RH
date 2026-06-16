from sqlalchemy import func

from app.daos.base_dao import BaseDAO
from app.extensions import db
from app.models.department import Department
from app.models.employee import Employee
from app.models.position import Position
from app.models.skill import Skill


class EmployeeDAO(BaseDAO):
    def __init__(self):
        super().__init__(Employee)

    def find_all(self):
        return Employee.query.order_by(Employee.created_at.desc()).all()

    def search(self, filters=None):
        filters = filters or {}
        query = Employee.query.join(Position).join(Department)

        name = (filters.get("name") or "").strip()
        department_id = filters.get("department_id")
        position_id = filters.get("position_id")
        status = filters.get("status")
        admission_start = filters.get("admission_start")
        admission_end = filters.get("admission_end")

        if name:
            query = query.filter(Employee.name.ilike(f"%{name}%"))
        if department_id:
            query = query.filter(Department.id == int(department_id))
        if position_id:
            query = query.filter(Position.id == int(position_id))
        if status:
            query = query.filter(Employee.status == status)
        if admission_start:
            query = query.filter(Employee.admission_date >= admission_start)
        if admission_end:
            query = query.filter(Employee.admission_date <= admission_end)

        return query.order_by(Employee.name.asc()).all()

    def create(self, data):
        skill_ids = data.pop("skill_ids", [])
        employee = Employee(**self._employee_fields(data))
        db.session.add(employee)
        db.session.flush()
        self._sync_skills(employee, skill_ids)
        db.session.commit()
        return employee

    def update(self, id, data):
        employee = self.find_by_id(id)
        if not employee:
            return None

        skill_ids = data.pop("skill_ids", None)
        for key, value in self._employee_fields(data).items():
            setattr(employee, key, value)

        if skill_ids is not None:
            self._sync_skills(employee, skill_ids)

        db.session.commit()
        return employee

    def count_by_status(self, status):
        return Employee.query.filter_by(status=status).count()

    def count_by_department(self):
        return (
            db.session.query(Department.name, func.count(Employee.id))
            .outerjoin(Position, Position.department_id == Department.id)
            .outerjoin(Employee, Employee.position_id == Position.id)
            .group_by(Department.id, Department.name)
            .order_by(Department.name.asc())
            .all()
        )

    def _employee_fields(self, data):
        allowed = {
            "position_id",
            "name",
            "email",
            "phone",
            "document",
            "birth_date",
            "admission_date",
            "status",
            "photo_path",
        }
        return {key: value for key, value in data.items() if key in allowed}

    def _sync_skills(self, employee, skill_ids):
        ids = [int(skill_id) for skill_id in skill_ids if str(skill_id).strip()]
        employee.skills = Skill.query.filter(Skill.id.in_(ids)).all() if ids else []
