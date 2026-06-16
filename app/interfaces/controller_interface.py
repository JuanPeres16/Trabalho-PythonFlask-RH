from abc import ABC, abstractmethod


class IController(ABC):
    @abstractmethod
    def index(self):
        pass

    @abstractmethod
    def show(self, id):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def store(self):
        pass

    @abstractmethod
    def edit(self, id):
        pass

    @abstractmethod
    def update(self, id):
        pass

    @abstractmethod
    def destroy(self, id):
        pass
