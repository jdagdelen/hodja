"""Chains are a collection of Links that are executed in order, with state passing from link to link.

Chains are the main components of Hodja. They are a collection of Links that are executed in order, with state passing from link to link. Chains are the main way to create a Hodja workflow. The user's input goes into the first Link in the Chain, and the output of the last Link in the Chain is the final output that returns to the user."""

from abc import ABC, abstractmethod


class Chain(ABC):
    def __init__(self, name, links=[], intial_state={}):
        self.name = name
        self.state = intial_state
        self.links = links

    def run(self, input, debug=False):
        """Run the chain by executing each link in order."""
        self.state["input"] = input
        for link in self.links:
            self.state = link.run(self.state, debug=debug)
        return self.state['output']
