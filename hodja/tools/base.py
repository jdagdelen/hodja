from abc import ABC, abstractmethod

class Tool(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError