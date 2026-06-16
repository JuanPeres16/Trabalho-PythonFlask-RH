from flask import Blueprint

from app.controllers.auth_controller import AuthController


auth_bp = Blueprint("auth", __name__)
controller = AuthController()


auth_bp.add_url_rule("/login", view_func=controller.login, methods=["GET", "POST"])
auth_bp.add_url_rule("/register", view_func=controller.register, methods=["GET", "POST"])
auth_bp.add_url_rule("/logout", view_func=controller.logout, methods=["GET", "POST"])
