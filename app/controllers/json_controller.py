from flask import Response, flash, redirect, render_template, request, url_for

from app.middlewares.validation_middleware import validate_json_file
from app.services.json_service import JsonService


class JsonController:
    def __init__(self):
        self.service = JsonService()

    def index(self):
        return render_template("imports/index.html")

    def export(self, entity):
        content = self.service.export_entity(entity)
        return Response(
            content,
            mimetype="application/json",
            headers={
                "Content-Disposition": f"attachment; filename={entity}.json",
            },
        )

    def import_entity(self, entity):
        file_storage = request.files.get("file")
        errors = validate_json_file(file_storage)
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("json.index"))

        try:
            imported = self.service.import_entity(entity, file_storage)
            flash(f"{imported} registro(s) importado(s) com sucesso.", "success")
        except Exception as error:
            flash(f"Nao foi possivel importar o JSON: {error}", "error")
        return redirect(url_for("json.index"))
