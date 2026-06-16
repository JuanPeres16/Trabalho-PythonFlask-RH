from flask import Blueprint

from app.controllers.json_controller import JsonController


json_bp = Blueprint("json", __name__)
controller = JsonController()


json_bp.add_url_rule("/imports", endpoint="index", view_func=controller.index, methods=["GET"])
json_bp.add_url_rule("/imports/<entity>", endpoint="import_entity", view_func=controller.import_entity, methods=["POST"])
json_bp.add_url_rule("/exports/<entity>.json", endpoint="export", view_func=controller.export, methods=["GET"])
