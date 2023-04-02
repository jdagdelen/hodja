"""Chains are a collection of Links that are executed in order, with state passing from link to link.

Chains are the main components of Hodja. They are a collection of Links that are executed in order, with state passing from link to link. Chains are the main way to create a Hodja workflow. The user's input goes into the first Link in the Chain, and the output of the last Link in the Chain is the final output that returns to the user."""

from abc import ABC, abstractmethod


class ChainBase(ABC):
    def __init__(self, name, links=[], intial_state={}):
        self.name = name
        self.state = intial_state
        self.links = links

    @abstractmethod
    def run(self):
        """Run the chain by executing each link in order."""
        raise NotImplementedError
