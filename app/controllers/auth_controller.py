from flask import flash, redirect, render_template, request, url_for

from app.services.auth_service import AuthService


class AuthController:
    def __init__(self):
        self.service = AuthService()

    def login(self):
        if request.method == "POST":
            user, error = self.service.login(
                request.form.get("email"), request.form.get("password")
            )
            if error:
                flash(error, "error")
                return redirect(url_for("auth.login"))

            flash(f"Bem-vindo, {user.name}!", "success")
            return redirect(url_for("dashboard.index"))

        return render_template("login.html")

    def register(self):
        if request.method == "POST":
            user, error = self.service.register(request.form)
            if error:
                flash(error, "error")
                return redirect(url_for("auth.register"))

            flash(f"Usuario {user.name} cadastrado com sucesso.", "success")
            return redirect(url_for("auth.login"))

        return render_template("register.html")

    def logout(self):
        self.service.logout()
        flash("Sessao encerrada com sucesso.", "success")
        return redirect(url_for("auth.login"))
