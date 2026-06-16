from flask import Blueprint

from app.controllers.chart_controller import ChartController


chart_bp = Blueprint("charts", __name__, url_prefix="/api/charts")
controller = ChartController()


chart_bp.add_url_rule(
    "/employees-by-department",
    endpoint="employees_by_department",
    view_func=controller.employees_by_department,
    methods=["GET"],
)
