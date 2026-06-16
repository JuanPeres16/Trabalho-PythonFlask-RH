from flask import Blueprint

from app.controllers.department_controller import DepartmentController


department_bp = Blueprint("departments", __name__, url_prefix="/departments")
controller = DepartmentController()


department_bp.add_url_rule("", endpoint="index", view_func=controller.index)
department_bp.add_url_rule("/create", endpoint="create", view_func=controller.create)
department_bp.add_url_rule("", endpoint="store", view_func=controller.store, methods=["POST"])
department_bp.add_url_rule("/<int:id>/edit", endpoint="edit", view_func=controller.edit)
department_bp.add_url_rule("/<int:id>", endpoint="update", view_func=controller.update, methods=["PUT"])
department_bp.add_url_rule("/<int:id>/update", endpoint="update_post", view_func=controller.update, methods=["POST"])
department_bp.add_url_rule("/<int:id>", endpoint="destroy", view_func=controller.destroy, methods=["DELETE"])
department_bp.add_url_rule("/<int:id>/delete", endpoint="destroy_post", view_func=controller.destroy, methods=["POST"])
