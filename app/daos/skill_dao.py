from app.daos.base_dao import BaseDAO
from app.models.skill import Skill


class SkillDAO(BaseDAO):
    def __init__(self):
        super().__init__(Skill)

    def find_by_name(self, name):
        return Skill.query.filter_by(name=name).first()
