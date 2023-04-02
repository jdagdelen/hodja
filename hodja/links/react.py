"""Link implementing ReACT (https://arxiv.org/abs/2210.03629)"""
from hodja.chains.base import Chain
from hodja.links.base import Link
from hodja.agents.openai import OpenAIAPIAgent

REACT_PROMPT = """You are a polite, thoughtful, and resourceful general purpose AI. 

Tools - You can use the following tools. The tool name is listed first and a description is listed after the colon.
{tool_summary}

To employ a tool, use following format:
    Action: <tool name>[<tool input>]

Note: You MUST use the tool's name (as provided above) in order to use a tool.
    
Instructions
------------
You work in a thought-action-observation cycle. In each cycle, you:
    1. Think about the problem and how to solve it.
    2. Perform an action. You can use one of the tools or return a final response with `RETURN[<final answer>]. You can only use one tool at a time.
    3. Observe the result of your action. This will be the output from any tool you used, or the final answer if you returned a final answer.
    4. Repeat steps 1-3 until you have a final answer in the observation.

Use the following format:

    Thought: <a thought>
    Action: <tool name>[<tool input>] (or RETURN[<final answer>])
    Observation: <action result>
    Thought: <a thought>
    Action: <tool name>[<tool input>] (or RETURN[<final answer>])
    Observation: <action result>
    ...

Example 1 (no tool needed):
    ```
    User Input: What is captial of France?
    Tools Available: ()
    Thought: I know that Paris is the capital of France.
    Action: RETURN[Paris]
    Observation: Paris
    ```

Example 2 (tool needed):
    In this example, assume that a Weather tool is available.
    ```
    User Input: What is the weather in Paris?
    Tools Available: (Weather)
    Thought: I need to use the Weather tool to get the weather in Paris.
    Action: Weather[Paris]
    Observation: ('city': 'Paris', 'country': 'France', 'temperature': 20, 'weather': 'sunny')
    Thought: I now know that it is 20 degrees and sunny in Paris.
    Action: RETURN[It is 20 degrees and sunny in Paris]
    Observation: It is 20 degrees and sunny in Paris.
    ```
    Note: the above is just an example. The Weather tool may not actually be available. Only use tools listed in the Tools Avaliable section.

Extra notes:
If a math or code tool is available, do not do any math yourself. Use Tools to evaluate math expressions.

Begin!

{workspace}"""

class ReACTLink(Link):
    """ A Link that uses the ReACT algorithm to generate reasoning traces and task-specific actions in an interleaved manner.
    
    Each step involves:
        1. Thought
        2. Action
        3. Observation
        
    """
    def __init__(self, agent=OpenAIAPIAgent(stop=['\n'], max_tokens=250), prompt=REACT_PROMPT, tools=[]):
        super().__init__(name="ReACTLink")
        self.agent = agent
        self.prompt = prompt
        self.tools = tools
        self.tool_names = str([tool.name for tool in self.tools]).replace("[", "(").replace("]", ")")
        self.tool_summary = "\n".join(["* " + str(tool) for tool in self.tools])

    def _parse_action(self, action):
        """Parse the output of the agent into a state dictionary."""
        # check if we have a final answer
        if "RETURN" in action:
            return {"final_answer": action.split("RETURN[")[1].split("]")[0]}
        else:
            # parse tool output
            tool_name = action.split("[")[0].strip()
            tool_input = action.split("[")[1].split("]")[0].strip()
            return {tool_name: tool_input}
        
    def validate_state(self, state):
        return True

    def _format_prompt(self, workspace):
        """Update the prompt with configuration and the current state of the workspace."""
        return self.prompt.format(
            tool_summary=self.tool_summary,
            workspace=workspace
        )
        
    def run(self, state, max_calls=5, debug=False):
        """Run the ReACT loop until a final answer is found or max_calls is reached."""

        # get input from state
        input = state["input"]
        workspace = f"User Input: {input}\nTools Available: {self.tool_names}"
        TAOs = []

        if debug: 
            print(self._format_prompt(workspace))

        # main loop
        terminate = False
        calls = 0
        while not terminate and calls < max_calls:
            # update prompt for next step
            TAO = {}
            # Think
            agent_input = self._format_prompt(workspace) + "Thought:"
            thought = self.agent(agent_input)
            TAO['thought'] = thought
            workspace += f"Thought: {thought}\n"
            if debug:
                print(f"Thought: {thought}")
            
            # Act
            agent_input = self._format_prompt(workspace) + "Action:"
            action = self.agent(agent_input)
            TAO['action'] = action
            workspace += f"Action: {action}\n"
            if debug:
                print(f"Action: {action}")
            
            # Observe
            parsed_action = self._parse_action(action)
            if "final_answer" in parsed_action:
                observation = parsed_action["final_answer"]
                TAO['observation'] = observation
                workspace += f"Observation: {observation}\n"
                if debug:
                    print(f"Observation: {observation}")
                state["output"] = parsed_action["final_answer"]
                terminate = True
            else:
                # check if we need to run a tool and run it
                for tool in self.tools:
                    if tool.name in parsed_action:
                        observation = tool.run(parsed_action[tool.name])
                        TAO['observation'] = observation
                        workspace += f"Observation: {observation}\n"
                        if debug:
                            print(f"Observation: {observation}")
                        break
            TAOs.append(TAO)
            calls += 1

        return state