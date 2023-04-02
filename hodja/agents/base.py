"""Base class for agents."""

from abc import ABC

class Agent(ABC):
    """Base class for agents."""

    def __init__(self, name):
        self.name = name

    def __call__(self, prompt, state, tools):
        """Run the agent."""
        raise NotImplementedError

    def prepare_prompt_string(self, prompt, state, tools):
        """Formats the prompts with information from state"""
        return prompt.format(**state, tools=tools)