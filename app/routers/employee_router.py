from flask import Blueprint

from app.controllers.employee_controller import EmployeeController


employee_bp = Blueprint("employees", __name__, url_prefix="/employees")
controller = EmployeeController()


employee_bp.add_url_rule("", endpoint="index", view_func=controller.index, methods=["GET"])
employee_bp.add_url_rule("/create", endpoint="create", view_func=controller.create, methods=["GET"])
employee_bp.add_url_rule("", endpoint="store", view_func=controller.store, methods=["POST"])
employee_bp.add_url_rule("/<int:id>", endpoint="show", view_func=controller.show, methods=["GET"])
employee_bp.add_url_rule("/<int:id>/edit", endpoint="edit", view_func=controller.edit, methods=["GET"])
employee_bp.add_url_rule("/<int:id>", endpoint="update", view_func=controller.update, methods=["PUT"])
employee_bp.add_url_rule("/<int:id>/update", endpoint="update_post", view_func=controller.update, methods=["POST"])
employee_bp.add_url_rule("/<int:id>", endpoint="destroy", view_func=controller.destroy, methods=["DELETE"])
employee_bp.add_url_rule("/<int:id>/delete", endpoint="destroy_post", view_func=controller.destroy, methods=["POST"])
