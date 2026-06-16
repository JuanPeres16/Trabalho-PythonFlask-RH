from flask import Blueprint

from app.controllers.position_controller import PositionController


position_bp = Blueprint("positions", __name__, url_prefix="/positions")
controller = PositionController()


position_bp.add_url_rule("", endpoint="index", view_func=controller.index)
position_bp.add_url_rule("/create", endpoint="create", view_func=controller.create)
position_bp.add_url_rule("", endpoint="store", view_func=controller.store, methods=["POST"])
position_bp.add_url_rule("/<int:id>/edit", endpoint="edit", view_func=controller.edit)
position_bp.add_url_rule("/<int:id>", endpoint="update", view_func=controller.update, methods=["PUT"])
position_bp.add_url_rule("/<int:id>/update", endpoint="update_post", view_func=controller.update, methods=["POST"])
position_bp.add_url_rule("/<int:id>", endpoint="destroy", view_func=controller.destroy, methods=["DELETE"])
position_bp.add_url_rule("/<int:id>/delete", endpoint="destroy_post", view_func=controller.destroy, methods=["POST"])
