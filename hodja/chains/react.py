"""Chain implementing ReACT (https://arxiv.org/abs/2210.03629)"""
from hodja.chains.base import ChainBase
from hodja.links import Link
from hodja.agents.openai import OpenAIAgent

REACT_PROMPT = """You are a polite, thoughtful, and resourceful general purpose AI. 

Tools - You can use the following tools. The tool name is listed first and a description is listed after the colon.
{tools}

To employ a tool, use following format:
    Action: <tool name>[<tool input>]

Note: You MUST use the tool's name (as provided above) in order to use a tool.
    
Instructions: 
    1. Think about the problem and how to solve it.
    2. Perform an action. You can use one of the tools or return a final response with `RETURN[<final answer>]
    3. Observe the result of your action. This will be the output from any tool you used, or the final answer if you returned a final answer.
    4. Repeat steps 1-3 until you have a final answer in the observation.

Use the following format:

    Thought: <a thought>
    Action: <tool name>[<tool input>] (or RETURN[<final answer>])
    Observation: <action result>
    ...

Example 1 (no tool needed):
    ```
    User: What is captial of France?
    Thought: I know that Paris is the capital of France.
    Action: RETURN[Paris]
    Observation: Paris
    ```

Example 2 (tool needed):
    In this example, assume that the Weather tool is available.
    ```
    User: What is the weather in Paris?
    Thought: I need to use the Weather tool to get the weather in Paris.
    Action: Weather[Paris]
    Observation: It is 20 degrees and sunny in Paris.
    Thought: I now know that it is 20 degrees and sunny in Paris.
    Action: RETURN[It is 20 degrees and sunny in Paris]
    Observation: It is 20 degrees and sunny in Paris.
    ```
    Note: the above is just an example. The Weather tool may not actually be available. Only use tools listed in the Tools section above.

Extra notes:
Do not do any math yourself. Use the Math tool to evaluate math expressions.

Begin!

{internal_state}
"""

class ReACTLink(Link):

    def __init__(self, agent=OpenAIAgent(stop=['\n\n', 'Observation:']), prompt=REACT_PROMPT, tools=[]):
        super().__init__(name="ReACTLink")
        self.agent = agent
        self.prompt = prompt
        self.tools = tools

    def _parse_agent_output(self, output):
        """Parse the output of the agent into a state dictionary."""
        # check if we have a final answer
        if "Action: RETURN" in output:
            return {"final_answer": output.split("Action: RETURN[")[1].split("]")[0]}
        elif "Action:" in output:
            # parse tool output
            tool_name = output.split("Action: ")[1].split("[")[0]
            tool_input = output.split("Action: ")[1].split("[")[1].split("]")[0]
            return {tool_name: tool_input}
        else:
            return {}
        
    def validate_state(self, state):
        return True
        
    def run(self, state, max_calls=5):
        """Run the ReACT loop until a final answer is found or max_calls is reached."""

        # get input from state
        input = state["input"]

        internal_state = f"User Input: {input}\nThought: "

        # set up initial prompt
        prompt = self.prompt.format(
            tools="\n".join(["* " + str(tool) for tool in self.tools]), 
            internal_state=internal_state
        )

        # main loop
        terminate = False
        calls = 0
        while not terminate and calls < max_calls:
            # call agent
            agent_output = self.agent(prompt)
            internal_state += agent_output
            agent_output = self._parse_agent_output(self.agent(prompt))
            calls += 1

            # check if we have a final answer
            if "final_answer" in agent_output:
                state["output"] = agent_output["final_answer"]
                terminate = True
            else:
                # run any tools
                for tool in self.tools:
                    if tool.name in agent_output:
                        tool_output = tool.run(agent_output[tool.name])
                        internal_state += f"""\nObservation: {tool_output}\nThought: """
                        break
            # update prompt
            prompt = self.prompt.format(
                tools="\n*".join([tool.instructions for tool in self.tools]),
                internal_state=internal_state
            )
        return state

class ReACTChain(ChainBase):
    """ A Chain that uses the ReACT algorithm to generate reasoning traces and task-specific actions in an interleaved manner.
    
    Each step involves:
        1. Thought
        2. Action
        3. Observation
        
    """
    def __init__(self, name, links, intial_state={}):
        super().__init__(name, links, intial_state)

    def run(self, input):
        """Run the chain"""
        self.state["input"] = input
        for link in self.links:
            self.state = link.run(self.state)
        return self.state['output']