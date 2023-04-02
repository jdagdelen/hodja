"""Links are the main components of Chains. 

Links take in input state, do work, and then pass output state to the next Link in the Chain. Links are usually composed of an Agent and zero or more Tools. A Link is responsible for processing the input state and creating the output state. Agents are intelligent agents that help do this task. The Tools are used by the Agent to perform the necessary tasks to create the ouput state. Links can enforce conditions on the input state they recieve. For example, a Link may require that there is a "date":<date> exists in the state. Links can choose to ignore parts of the chain state that they don't need."""

from abc import ABC, abstractmethod

class Link(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def validate_state(self, state):
        """Validate the input state. Raise an exception if the input state is invalid for this Link."""
        raise NotImplementedError

    @abstractmethod
    def run(self, input_state, **kwargs):
        """Run the link. Return the output state."""
        raise NotImplementedError