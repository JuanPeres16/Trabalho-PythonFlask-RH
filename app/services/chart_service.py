from app.daos.employee_dao import EmployeeDAO


class ChartService:
    def __init__(self):
        self.employee_dao = EmployeeDAO()

    def employees_by_department(self):
        rows = self.employee_dao.count_by_department()
        return {
            "labels": [name for name, _total in rows],
            "data": [int(total) for _name, total in rows],
        }
