from flask import Blueprint

from app.controllers.report_controller import ReportController


report_bp = Blueprint("reports", __name__)
controller = ReportController()


report_bp.add_url_rule("/reports/employees", endpoint="employees", view_func=controller.employees, methods=["GET"])
report_bp.add_url_rule("/reports/employees/pdf", endpoint="employees_pdf", view_func=controller.employees_pdf, methods=["GET"])
