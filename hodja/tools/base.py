from abc import ABC, abstractmethod

class Tool(ABC):
    def __init__(self, name, description, instructions):
        self.name = name
        self.description = description
        self.instructions = instructions

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.name}: {self.description}"
    
    def __str__(self):
        return self.__repr__()