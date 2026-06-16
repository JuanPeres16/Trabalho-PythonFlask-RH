from app.daos.skill_dao import SkillDAO
from app.interfaces.service_interface import IService
from app.services.log_service import LogService


class SkillService(IService):
    def __init__(self):
        self.dao = SkillDAO()
        self.log_service = LogService()

    def list(self):
        return self.dao.find_all()

    def get(self, id):
        return self.dao.find_by_id(id)

    def store(self, data):
        skill = self.dao.create({"name": (data.get("name") or "").strip()})
        self.log_service.save_log("CREATE", "cadastro", "skills", skill.id, skill.to_dict())
        return skill

    def update(self, id, data):
        skill = self.dao.update(id, {"name": (data.get("name") or "").strip()})
        if skill:
            self.log_service.save_log(
                "UPDATE", "alteracao", "skills", skill.id, skill.to_dict()
            )
        return skill

    def delete(self, id):
        deleted = self.dao.delete(id)
        if deleted:
            self.log_service.save_log("DELETE", "exclusao", "skills", id)
        return deleted
