from flask import Response, render_template, request

from app.services.log_service import LogService
from app.services.xml_service import XmlService


class LogController:
    def __init__(self):
        self.log_service = LogService()
        self.xml_service = XmlService()

    def index(self):
        logs = self.log_service.query_logs(request.args, limit=200)
        return render_template("logs/index.html", logs=logs, filters=request.args)

    def export_xml(self):
        logs = self.log_service.query_logs(request.args, limit=1000)
        content = self.xml_service.logs_to_xml(logs)
        self.log_service.save_log(
            "EXPORT_XML", "exportacao_xml", "logs", None, {"total": len(logs)}
        )
        return Response(
            content,
            mimetype="application/xml",
            headers={"Content-Disposition": "attachment; filename=logs.xml"},
        )
