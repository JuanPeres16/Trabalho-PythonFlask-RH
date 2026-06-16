from flask import render_template, request, send_file, session

from app.daos.department_dao import DepartmentDAO
from app.daos.position_dao import PositionDAO
from app.services.employee_service import EmployeeService
from app.services.log_service import LogService
from app.services.pdf_service import PdfService


class ReportController:
    def __init__(self):
        self.employee_service = EmployeeService()
        self.department_dao = DepartmentDAO()
        self.position_dao = PositionDAO()
        self.pdf_service = PdfService()
        self.log_service = LogService()

    def employees(self):
        employees = self.employee_service.list(request.args)
        return render_template(
            "reports/employees.html",
            employees=employees,
            departments=self.department_dao.find_all(),
            positions=self.position_dao.find_all(),
            filters=request.args,
        )

    def employees_pdf(self):
        employees = self.employee_service.list(request.args)
        generated_by = session.get("user_name", "Usuario")
        pdf = self.pdf_service.employees_report(employees, generated_by)
        self.log_service.save_log(
            "GENERATE_PDF",
            "relatorio_pdf",
            "employees",
            None,
            {"total": len(employees)},
        )
        return send_file(
            pdf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="relatorio_colaboradores.pdf",
        )
