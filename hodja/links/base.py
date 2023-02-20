from abc import ABC, abstractmethod

class Link(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def validate_input_state(self, input_state):
        """Validate the input state. Raise an exception if the input state is invalid for this Link."""
        pass

    @abstractmethod
    def run(self, input_state, **kwargs):
        pass