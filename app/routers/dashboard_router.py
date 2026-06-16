from flask import Blueprint

from app.controllers.dashboard_controller import DashboardController


dashboard_bp = Blueprint("dashboard", __name__)
controller = DashboardController()


dashboard_bp.add_url_rule(
    "/dashboard", endpoint="index", view_func=controller.index, methods=["GET"]
)
