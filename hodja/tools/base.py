from abc import ABC, abstractmethod

class Tool(ABC):
    def __init__(self, name, description, instructions):
        self.name = name
        self.description = description
        self.instructions = instructions

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError