from app.routers.auth_router import auth_bp
from app.routers.chart_router import chart_bp
from app.routers.dashboard_router import dashboard_bp
from app.routers.department_router import department_bp
from app.routers.employee_router import employee_bp
from app.routers.json_router import json_bp
from app.routers.log_router import log_bp
from app.routers.position_router import position_bp
from app.routers.report_router import report_bp
from app.routers.skill_router import skill_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(position_bp)
    app.register_blueprint(skill_bp)
    app.register_blueprint(json_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(chart_bp)
