from flask import flash, jsonify, redirect, render_template, request, url_for

from app.daos.department_dao import DepartmentDAO
from app.daos.position_dao import PositionDAO
from app.daos.skill_dao import SkillDAO
from app.interfaces.controller_interface import IController
from app.middlewares.validation_middleware import validate_employee_form
from app.services.employee_service import EmployeeService


class EmployeeController(IController):
    def __init__(self):
        self.service = EmployeeService()
        self.department_dao = DepartmentDAO()
        self.position_dao = PositionDAO()
        self.skill_dao = SkillDAO()

    def index(self):
        employees = self.service.list(request.args)
        return render_template(
            "employees/index.html",
            employees=employees,
            departments=self.department_dao.find_all(),
            positions=self.position_dao.find_all(),
            filters=request.args,
        )

    def show(self, id):
        employee = self.service.get(id)
        if not employee:
            flash("Colaborador nao encontrado.", "error")
            return redirect(url_for("employees.index"))
        return render_template("employees/show.html", employee=employee)

    def create(self):
        return render_template("employees/create.html", **self._form_options())

    def store(self):
        data = request.get_json() if request.is_json else request.form
        photo_file = request.files.get("photo")
        errors = validate_employee_form(data, photo_file)
        if errors:
            if request.is_json:
                return jsonify({"errors": errors}), 422
            for error in errors:
                flash(error, "error")
            return redirect(url_for("employees.create"))

        employee = self.service.store({"form": data, "photo_file": photo_file})
        if request.is_json:
            return jsonify(employee.to_dict()), 201
        flash("Colaborador cadastrado com sucesso.", "success")
        return redirect(url_for("employees.show", id=employee.id))

    def edit(self, id):
        employee = self.service.get(id)
        if not employee:
            flash("Colaborador nao encontrado.", "error")
            return redirect(url_for("employees.index"))
        return render_template("employees/edit.html", employee=employee, **self._form_options())

    def update(self, id):
        data = request.get_json() if request.is_json else request.form
        photo_file = request.files.get("photo")
        errors = validate_employee_form(data, photo_file)
        if errors:
            if request.method == "PUT" or request.is_json:
                return jsonify({"errors": errors}), 422
            for error in errors:
                flash(error, "error")
            return redirect(url_for("employees.edit", id=id))

        employee = self.service.update(id, {"form": data, "photo_file": photo_file})
        if request.method == "PUT" or request.is_json:
            return jsonify(employee.to_dict() if employee else {}), 200
        flash("Colaborador atualizado com sucesso.", "success")
        return redirect(url_for("employees.show", id=id))

    def destroy(self, id):
        deleted = self.service.delete(id)
        if request.method == "DELETE":
            return jsonify({"deleted": deleted}), 200 if deleted else 404
        flash("Colaborador excluido com sucesso." if deleted else "Colaborador nao encontrado.", "success" if deleted else "error")
        return redirect(url_for("employees.index"))

    def _form_options(self):
        return {
            "departments": self.department_dao.find_all(),
            "positions": self.position_dao.find_all(),
            "skills": self.skill_dao.find_all(),
        }
