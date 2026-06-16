from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from app.daos.user_dao import UserDAO
from app.services.log_service import LogService


class AuthService:
    def __init__(self):
        self.user_dao = UserDAO()
        self.log_service = LogService()

    def register(self, data):
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""

        if not name or not email or not password:
            return None, "Preencha nome, e-mail e senha."

        if self.user_dao.find_by_email(email):
            return None, "Este e-mail ja esta cadastrado."

        user = self.user_dao.create(
            {
                "name": name,
                "email": email,
                "password": generate_password_hash(password),
            }
        )
        self.log_service.save_log(
            "REGISTER", "cadastro_usuario", "users", user.id, {"email": user.email}
        )
        return user, None

    def login(self, email, password):
        email = (email or "").strip().lower()
        user = self.user_dao.find_by_email(email)

        if not user or not check_password_hash(user.password, password or ""):
            self.log_service.save_log(
                "LOGIN_FAIL", "autenticacao", "users", None, {"email": email}
            )
            return None, "E-mail ou senha invalidos."

        session["user_id"] = user.id
        session["user_name"] = user.name
        session["user_email"] = user.email
        self.log_service.save_log(
            "LOGIN_SUCCESS", "autenticacao", "users", user.id, {"email": user.email}
        )
        return user, None

    def logout(self):
        self.log_service.save_log("LOGOUT", "autenticacao", "users", session.get("user_id"))
        session.clear()
