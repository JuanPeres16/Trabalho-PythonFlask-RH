from app.daos.position_dao import PositionDAO
from app.interfaces.service_interface import IService
from app.services.log_service import LogService


class PositionService(IService):
    def __init__(self):
        self.dao = PositionDAO()
        self.log_service = LogService()

    def list(self):
        return self.dao.find_all()

    def get(self, id):
        return self.dao.find_by_id(id)

    def store(self, data):
        position = self.dao.create(
            {
                "department_id": int(data.get("department_id")),
                "name": (data.get("name") or "").strip(),
                "description": (data.get("description") or "").strip() or None,
            }
        )
        self.log_service.save_log(
            "CREATE", "cadastro", "positions", position.id, position.to_dict()
        )
        return position

    def update(self, id, data):
        position = self.dao.update(
            id,
            {
                "department_id": int(data.get("department_id")),
                "name": (data.get("name") or "").strip(),
                "description": (data.get("description") or "").strip() or None,
            },
        )
        if position:
            self.log_service.save_log(
                "UPDATE", "alteracao", "positions", position.id, position.to_dict()
            )
        return position

    def delete(self, id):
        deleted = self.dao.delete(id)
        if deleted:
            self.log_service.save_log("DELETE", "exclusao", "positions", id)
        return deleted
