from flask import jsonify, redirect, request, session, url_for


PUBLIC_PATHS = {"/", "/login", "/register", "/favicon.ico"}


def init_auth_middleware(app):
    @app.before_request
    def require_login():
        if request.path in PUBLIC_PATHS or request.path.startswith("/static"):
            return None

        if session.get("user_id"):
            return None

        if request.path.startswith("/api"):
            return jsonify({"error": "Nao autenticado."}), 401

        return redirect(url_for("auth.login"))
