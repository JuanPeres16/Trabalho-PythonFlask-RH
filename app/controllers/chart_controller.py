from flask import jsonify

from app.services.chart_service import ChartService


class ChartController:
    def __init__(self):
        self.service = ChartService()

    def employees_by_department(self):
        return jsonify(self.service.employees_by_department())
