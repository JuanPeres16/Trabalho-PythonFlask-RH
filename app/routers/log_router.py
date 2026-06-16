from flask import Blueprint

from app.controllers.log_controller import LogController


log_bp = Blueprint("logs", __name__)
controller = LogController()


log_bp.add_url_rule("/logs", endpoint="index", view_func=controller.index, methods=["GET"])
log_bp.add_url_rule("/logs/export.xml", endpoint="export_xml", view_func=controller.export_xml, methods=["GET"])
