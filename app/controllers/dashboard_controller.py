from flask import render_template

from app.daos.department_dao import DepartmentDAO
from app.daos.position_dao import PositionDAO
from app.daos.skill_dao import SkillDAO
from app.services.employee_service import EmployeeService
from app.services.log_service import LogService


class DashboardController:
    def __init__(self):
        self.employee_service = EmployeeService()
        self.department_dao = DepartmentDAO()
        self.position_dao = PositionDAO()
        self.skill_dao = SkillDAO()
        self.log_service = LogService()

    def index(self):
        return render_template(
            "dashboard.html",
            total_employees=self.employee_service.total(),
            total_departments=len(self.department_dao.find_all()),
            total_positions=len(self.position_dao.find_all()),
            total_skills=len(self.skill_dao.find_all()),
            active_employees=self.employee_service.total_by_status("ativo"),
            inactive_employees=self.employee_service.total_by_status("inativo"),
            logs=self.log_service.query_logs(limit=8),
        )
