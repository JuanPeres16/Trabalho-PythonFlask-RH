from app.daos.base_dao import BaseDAO
from app.models.user import User


class UserDAO(BaseDAO):
    def __init__(self):
        super().__init__(User)

    def find_by_email(self, email):
        return User.query.filter_by(email=email).first()
