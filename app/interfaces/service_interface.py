from abc import ABC, abstractmethod


class IService(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def store(self, data):
        pass

    @abstractmethod
    def update(self, id, data):
        pass

    @abstractmethod
    def delete(self, id):
        pass
