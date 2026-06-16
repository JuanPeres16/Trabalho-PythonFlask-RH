from app.daos.base_dao import BaseDAO
from app.models.position import Position


class PositionDAO(BaseDAO):
    def __init__(self):
        super().__init__(Position)

    def find_all(self):
        return Position.query.order_by(Position.name.asc()).all()

    def find_by_name(self, name):
        return Position.query.filter_by(name=name).first()
