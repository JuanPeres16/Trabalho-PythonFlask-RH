from flask import flash, jsonify, redirect, render_template, request, url_for

from app.daos.department_dao import DepartmentDAO
from app.interfaces.controller_interface import IController
from app.middlewares.validation_middleware import validate_position_form
from app.services.position_service import PositionService


class PositionController(IController):
    def __init__(self):
        self.service = PositionService()
        self.department_dao = DepartmentDAO()

    def index(self):
        return render_template("positions/index.html", positions=self.service.list())

    def show(self, id):
        return redirect(url_for("positions.index"))

    def create(self):
        return render_template(
            "positions/create.html", departments=self.department_dao.find_all()
        )

    def store(self):
        errors = validate_position_form(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("positions.create"))

        self.service.store(request.form)
        flash("Cargo cadastrado com sucesso.", "success")
        return redirect(url_for("positions.index"))

    def edit(self, id):
        position = self.service.get(id)
        if not position:
            flash("Cargo nao encontrado.", "error")
            return redirect(url_for("positions.index"))
        return render_template(
            "positions/edit.html",
            position=position,
            departments=self.department_dao.find_all(),
        )

    def update(self, id):
        data = request.get_json() if request.is_json else request.form
        errors = validate_position_form(data)
        if errors:
            if request.method == "PUT":
                return jsonify({"errors": errors}), 422
            for error in errors:
                flash(error, "error")
            return redirect(url_for("positions.edit", id=id))

        position = self.service.update(id, data)
        if request.method == "PUT":
            return jsonify(position.to_dict() if position else {}), 200
        flash("Cargo atualizado com sucesso.", "success")
        return redirect(url_for("positions.index"))

    def destroy(self, id):
        deleted = self.service.delete(id)
        if request.method == "DELETE":
            return jsonify({"deleted": deleted}), 200 if deleted else 404
        flash("Cargo excluido com sucesso." if deleted else "Cargo nao encontrado.", "success" if deleted else "error")
        return redirect(url_for("positions.index"))
