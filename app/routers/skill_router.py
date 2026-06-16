from flask import Blueprint

from app.controllers.skill_controller import SkillController


skill_bp = Blueprint("skills", __name__, url_prefix="/skills")
controller = SkillController()


skill_bp.add_url_rule("", endpoint="index", view_func=controller.index)
skill_bp.add_url_rule("/create", endpoint="create", view_func=controller.create)
skill_bp.add_url_rule("", endpoint="store", view_func=controller.store, methods=["POST"])
skill_bp.add_url_rule("/<int:id>/edit", endpoint="edit", view_func=controller.edit)
skill_bp.add_url_rule("/<int:id>", endpoint="update", view_func=controller.update, methods=["PUT"])
skill_bp.add_url_rule("/<int:id>/update", endpoint="update_post", view_func=controller.update, methods=["POST"])
skill_bp.add_url_rule("/<int:id>", endpoint="destroy", view_func=controller.destroy, methods=["DELETE"])
skill_bp.add_url_rule("/<int:id>/delete", endpoint="destroy_post", view_func=controller.destroy, methods=["POST"])
