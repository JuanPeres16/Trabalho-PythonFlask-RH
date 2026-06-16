import os

from flask import Flask, redirect, session, url_for
from werkzeug.security import generate_password_hash

from app.config import Config
from app.extensions import db, migrate, mongo
from app.middlewares.auth_middleware import init_auth_middleware
from app.middlewares.error_middleware import init_error_middleware
from app.middlewares.log_middleware import init_log_middleware
from app.middlewares.validation_middleware import init_validation_middleware
from app.models import Department, Position, Skill, User
from app.routers import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.ensure_ascii = False

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    mongo.init_app(app)

    register_blueprints(app)
    init_log_middleware(app)
    init_auth_middleware(app)
    init_validation_middleware(app)
    init_error_middleware(app)
    register_cli(app)

    @app.context_processor
    def inject_globals():
        return {
            "app_name": app.config["APP_NAME"],
            "current_user_name": session.get("user_name"),
            "current_user_email": session.get("user_email"),
        }

    @app.route("/")
    def home():
        if session.get("user_id"):
            return redirect(url_for("dashboard.index"))
        return redirect(url_for("auth.login"))

    return app


def register_cli(app):
    @app.cli.command("seed")
    def seed():
        db.create_all()

        if not User.query.filter_by(email="admin@peopleflow.com").first():
            admin = User(
                name="Administrador",
                email="admin@peopleflow.com",
                password=generate_password_hash("admin123"),
            )
            db.session.add(admin)

        departments = {}
        for name in ["Tecnologia", "RH", "Financeiro", "Vendas"]:
            department = Department.query.filter_by(name=name).first()
            if not department:
                department = Department(name=name, description=f"Departamento de {name}")
                db.session.add(department)
                db.session.flush()
            departments[name] = department

        seed_positions = [
            ("Desenvolvedor", "Tecnologia"),
            ("Analista de RH", "RH"),
            ("Analista Financeiro", "Financeiro"),
            ("Vendedor", "Vendas"),
        ]
        for name, department_name in seed_positions:
            exists = Position.query.filter_by(name=name).first()
            if not exists:
                db.session.add(
                    Position(
                        name=name,
                        description=f"Cargo de {name}",
                        department_id=departments[department_name].id,
                    )
                )

        for name in ["Python", "Flask", "Excel", "Comunicacao", "Lideranca"]:
            if not Skill.query.filter_by(name=name).first():
                db.session.add(Skill(name=name))

        db.session.commit()
        print("Seed concluido: admin, departamentos, cargos e habilidades criados.")
