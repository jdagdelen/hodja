"""Main components of Chains. Links take in input state, do work, and then pass output state to the next Link in the Chain.

Links are composed of an Agent and one or more Tools. The Agent is responsible for processing the input state and creating the output state. The Tools are used by the Agent to perform the necessary tasks to create the ouput state. Links can enforce conditions on the input state they recieve. For example, a Link may require the conversation history as a string. Links can choose to ignore parts of the chain state that they don't need."""

