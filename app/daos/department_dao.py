from app.daos.base_dao import BaseDAO
from app.models.department import Department


class DepartmentDAO(BaseDAO):
    def __init__(self):
        super().__init__(Department)

    def find_by_name(self, name):
        return Department.query.filter_by(name=name).first()
