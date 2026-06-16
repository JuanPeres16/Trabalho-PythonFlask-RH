from flask import flash, jsonify, redirect, render_template, request, url_for

from app.interfaces.controller_interface import IController
from app.middlewares.validation_middleware import validate_skill_form
from app.services.skill_service import SkillService


class SkillController(IController):
    def __init__(self):
        self.service = SkillService()

    def index(self):
        return render_template("skills/index.html", skills=self.service.list())

    def show(self, id):
        return redirect(url_for("skills.index"))

    def create(self):
        return render_template("skills/create.html")

    def store(self):
        errors = validate_skill_form(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for("skills.create"))

        self.service.store(request.form)
        flash("Habilidade cadastrada com sucesso.", "success")
        return redirect(url_for("skills.index"))

    def edit(self, id):
        skill = self.service.get(id)
        if not skill:
            flash("Habilidade nao encontrada.", "error")
            return redirect(url_for("skills.index"))
        return render_template("skills/edit.html", skill=skill)

    def update(self, id):
        data = request.get_json() if request.is_json else request.form
        errors = validate_skill_form(data)
        if errors:
            if request.method == "PUT":
                return jsonify({"errors": errors}), 422
            for error in errors:
                flash(error, "error")
            return redirect(url_for("skills.edit", id=id))

        skill = self.service.update(id, data)
        if request.method == "PUT":
            return jsonify(skill.to_dict() if skill else {}), 200
        flash("Habilidade atualizada com sucesso.", "success")
        return redirect(url_for("skills.index"))

    def destroy(self, id):
        deleted = self.service.delete(id)
        if request.method == "DELETE":
            return jsonify({"deleted": deleted}), 200 if deleted else 404
        flash("Habilidade excluida com sucesso." if deleted else "Habilidade nao encontrada.", "success" if deleted else "error")
        return redirect(url_for("skills.index"))
