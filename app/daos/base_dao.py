from app.extensions import db
from app.interfaces.dao_interface import IDAO


class BaseDAO(IDAO):
    model = None

    def __init__(self, model=None):
        if model is not None:
            self.model = model

    def find_all(self):
        return self.model.query.order_by(self.model.id.desc()).all()

    def find_by_id(self, id):
        return db.session.get(self.model, id)

    def create(self, data):
        instance = self.model(**data)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, id, data):
        instance = self.find_by_id(id)
        if not instance:
            return None

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        db.session.commit()
        return instance

    def delete(self, id):
        instance = self.find_by_id(id)
        if not instance:
            return False

        db.session.delete(instance)
        db.session.commit()
        return True
