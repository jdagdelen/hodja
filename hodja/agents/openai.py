"""Classes for interacting with OpenAI's API."""
import os
from hodja.agents.base import Agent
import openai
from collections import defaultdict

# create default dict of context sizes
CONTEXT_SIZES = defaultdict(lambda: 2048)
_defaults = {
    "text-davinci-003": 4097,
    "text-curie-001": 2048,
    "text-babbage-001": 2048,
    "text-ada-001": 2048,
    "code-davinci-002": 8000,
    "code-cushman-001": 2048,
    "gpt-3.5-turbo": 4097,
}
for k, v in _defaults.items():
    CONTEXT_SIZES[k] = v

class OpenAIAPIAgent(Agent):
    
    def __init__(
        self, 
        name='OpenAI Agent',
        api_key=os.getenv('OPENAI_API_KEY'),
        engine='text-davinci-003',
        temperature=0.0,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['\n\n',],
        streaming=False
        ):
        super().__init__(name=name)
        self.api_key = api_key
        self.engine = engine
        self.context_size = CONTEXT_SIZES[self.engine]
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.streaming = streaming

    def __call__(self, prompt):
        if len(prompt) + self.max_tokens > self.context_size:
            raise ValueError(
                f"Prompt length ({len(prompt)}) + max_tokens ({self.max_tokens}) "
                f"exceeds maximum context size ({self.context_size})."
            )
        results = openai.Completion.create(
            prompt=prompt,
            engine=self.engine,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            stop=self.stop,
            stream=self.streaming
        )
        return results.choices[0].text