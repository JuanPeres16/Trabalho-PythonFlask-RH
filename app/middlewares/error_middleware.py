from flask import jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from app.services.log_service import LogService


def init_error_middleware(app):
    @app.errorhandler(Exception)
    def handle_exception(error):
        status_code = error.code if isinstance(error, HTTPException) else 500

        if status_code >= 500:
            LogService().save_error(error)

        if request.path.startswith("/api"):
            return (
                jsonify(
                    {
                        "error": "Ocorreu um erro ao processar a requisicao.",
                        "status_code": status_code,
                    }
                ),
                status_code,
            )

        return (
            render_template(
                "error.html",
                status_code=status_code,
                message="Nao foi possivel concluir a operacao.",
            ),
            status_code,
        )
