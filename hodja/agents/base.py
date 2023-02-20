"""Base class for agents."""

from abc import ABC

class Agent(ABC):
    """Base class for agents."""

    def __init__(self, name):
        self.name = name

    def run(self, *args, **kwargs):
        pass