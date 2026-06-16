from flask import flash, jsonify, redirect, render_template, request, url_for

from app.interfaces.controller_interface import IController
from app.middlewares.validation_middleware import validate_department_form
from app.services.department_service import DepartmentService


class DepartmentController(IController):
    def __init__(self):
        self.service = DepartmentService()

    def index(self):
        return render_template("departments/index.html", departments=self.service.list())

    def show(self, id):
        return redirect(url_for("departments.index"))

    def create(self):
        return render_template("departments/create.html")

    def store(self):
        errors = validate_department_form(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("departments.create"))

        self.service.store(request.form)
        flash("Departamento cadastrado com sucesso.", "success")
        return redirect(url_for("departments.index"))

    def edit(self, id):
        department = self.service.get(id)
        if not department:
            flash("Departamento nao encontrado.", "error")
            return redirect(url_for("departments.index"))
        return render_template("departments/edit.html", department=department)

    def update(self, id):
        data = request.get_json() if request.is_json else request.form
        errors = validate_department_form(data)
        if errors:
            if request.method == "PUT":
                return jsonify({"errors": errors}), 422
            for error in errors:
                flash(error, "error")
            return redirect(url_for("departments.edit", id=id))

        department = self.service.update(id, data)
        if request.method == "PUT":
            return jsonify(department.to_dict() if department else {}), 200
        flash("Departamento atualizado com sucesso.", "success")
        return redirect(url_for("departments.index"))

    def destroy(self, id):
        deleted = self.service.delete(id)
        if request.method == "DELETE":
            return jsonify({"deleted": deleted}), 200 if deleted else 404
        flash("Departamento excluido com sucesso." if deleted else "Departamento nao encontrado.", "success" if deleted else "error")
        return redirect(url_for("departments.index"))
