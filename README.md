<p align="center">
  <img src="static/nasreddin_hodja_chain.png" alt="Nasreddin Hodja inspects a chain" width="200" />
</p>

# Hodja
Hodja is a framework for building [augmented language model](https://arxiv.org/abs/2302.07842)-based applications.

## About
Hodja is an attempt at creating a streamlined and focused framework for building chains of transformations that use natural language as their interface. I found other projects that take a more "kitchen sink" approach such as [langchain](https://github.com/hwchase17/langchain) were hard to use and debug in practice, so I decided to create my own.

The main concepts in Hodja are:

### Chains
A Chain is made up of a sequence of Links. Chains take in an intial input and pass it through each link in the Chain. The output of each Link is passed to the next subsequent Link in the Chain. The output of the final Link in the Chain is the output of the Chain. Information gets passed through the Chain in the form of a state.

### Links
A Link is responsible for taking in a state, making decisions about what to do, transforming the state based on those decisions, and then returning the new state. Links are the building blocks of Chains and are the main way to extend Hodja's functionality. Links contain Agents that are reponsible for making decisions about what to do. Complex functionality is built by combining Links together in Chains.

### Agents
An Agent lives inside a Link and is responsible for making decisions about what to do with the state. Agents can be simple, such as a function that uses regular expressions to extract information from a string, but they are usually more complex and based on large language models (LLMs). Agents need instructions to know what to do with the input state. We give Agents instructions in the form of **prompt strings**, which are just strings that are filled in with instructions and information from the state. Hodja contains a Prompt class for dynamically constructing prompt strings. Agents can also use Tools that augment them with new capabilities. To create a new Agent, we combine a LLM with a custom Prompt and one or more Tools. 

### Prompts
Prompts are objects that dynamically construct prompt strings. Prompts are read by Agents to determine what to do with the state. Prompts are constructed using a simple templating language that allows you to insert information from the state into the prompt string. Prompts can also dynamically decide what to put in the prompt string based on the state, for example providing more or less context to the Agent.

### Tools
A Tool is a object that can be used by an Agent to augment its capabilities, for example doing simple math expressions or performing a Google search. Tools are used by Agents to perform tasks that they are not able to do by themselves. Tools expose their functionality through a specific interface that allows any Agent to interact with them, and they need to come with "usage instructions" so that Agents will know how to use them at runtime. Almost anything can be wrapped into a Tool. The most common types of Tools expose an external API to Agents (WolframAlphaTool, etc.), give them additional functionality like math or regex operations (MathTool, RegexTool, etc.) or give Agents a way to work with external document stores (e.g. a SearchTool wrapped around a VectorStore.) Entire Chains can be wrapped into Tools, allowing Agents to use the functionality of other Chains.


## Installation
Clone this repository and in the root directory run:
```python setup.py install```

## Name
The name "Hodja" comes from "[Nasreddin Hodja](https://en.wikipedia.org/wiki/Nasreddin_)" who was a philosopher from what is now modern-day Turkey. His is known for his wit and wisdom, and is the main character of many humerous folk stories.

