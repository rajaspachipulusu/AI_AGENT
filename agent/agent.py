from llm.llm import LLM

from agent.prompts import SYSTEM_PROMPT

from tools.registry import ToolRegistry
from tools.calculator import CalculatorTool
from tools.csv_tool import CSVTool
from tools.web_search import WebSearchTool


class Agent:

    def __init__(self):

        # ----------------------------------
        # Initialize LLM
        # ----------------------------------

        self.llm = LLM()

        # ----------------------------------
        # Initialize Tool Registry
        # ----------------------------------

        self.registry = ToolRegistry()

        # Register available tools

        self.registry.register(
            CalculatorTool
        )

        self.registry.register(
            CSVTool
        )

        self.registry.register(
            WebSearchTool
        )

    def run(self, question):

        # ----------------------------------
        # Build Tool Description
        # ----------------------------------

        tool_descriptions = (
            self.registry.describe_tools()
        )

        # ----------------------------------
        # Build System Prompt
        # ----------------------------------

        system_prompt = SYSTEM_PROMPT.format(
            tools=tool_descriptions
        )

        # ----------------------------------
        # Agent Messages / State
        # ----------------------------------

        messages = [
            system_prompt,
            f"User question:\n{question}"
        ]

        # ----------------------------------
        # Maximum Agent Steps
        # ----------------------------------

        max_steps = 5

        # ----------------------------------
        # Agent Loop
        # ----------------------------------

        for step in range(max_steps):

            print(
                f"\n========== Agent Step "
                f"{step + 1} =========="
            )

            # ----------------------------------
            # Build Prompt
            # ----------------------------------

            prompt = "\n\n".join(messages)

            # ----------------------------------
            # Ask LLM
            # ----------------------------------

            response = self.llm.generate(prompt)

            print("\nLLM Response:")
            print(response)

            # ----------------------------------
            # FINAL ANSWER
            # ----------------------------------

            if response.startswith("ANSWER:"):

                return response.replace(
                    "ANSWER:",
                    "",
                    1
                ).strip()

            # ----------------------------------
            # TOOL CALL
            # ----------------------------------

            if response.startswith("TOOL:"):

                tool_name = None
                tool_input = None

                # ----------------------------------
                # Parse Tool Response
                # ----------------------------------

                for line in response.splitlines():

                    if line.startswith("TOOL:"):

                        tool_name = line.replace(
                            "TOOL:",
                            "",
                            1
                        ).strip()

                    elif line.startswith("INPUT:"):

                        tool_input = line.replace(
                            "INPUT:",
                            "",
                            1
                        ).strip()

                # ----------------------------------
                # Validate Tool Request
                # ----------------------------------

                if not tool_name:

                    messages.append(
                        """
Your tool request did not contain
a valid tool name.

Please return:

TOOL: <tool name>
INPUT: <tool input>
"""
                    )

                    continue

                if not tool_input:

                    messages.append(
                        """
Your tool request did not contain
valid tool input.

Please return:

TOOL: <tool name>
INPUT: <tool input>
"""
                    )

                    continue

                # ----------------------------------
                # Find Tool
                # ----------------------------------

                tool = self.registry.get(
                    tool_name
                )

                if tool is None:

                    messages.append(
                        f"""
The requested tool does not exist:

{tool_name}

Available tools are:

{self.registry.describe_tools()}

Choose a valid tool.
"""
                    )

                    continue

                # ----------------------------------
                # Display Tool Call
                # ----------------------------------

                print(
                    f"\nCalling Tool: {tool_name}"
                )

                print(
                    f"Tool Input: {tool_input}"
                )

                # ----------------------------------
                # Execute Tool
                # ----------------------------------

                try:

                    result = tool.run(
                        tool_input
                    )

                except Exception as e:

                    result = {
                        "status": "error",
                        "message": str(e)
                    }

                # ----------------------------------
                # Display Tool Result
                # ----------------------------------

                print(
                    f"Tool Result: {result}"
                )

                # ----------------------------------
                # Add Tool Observation
                # ----------------------------------

                messages.append(
                    f"""
Tool: {tool_name}

Input:
{tool_input}

Tool Result:
{result}

IMPORTANT:

If the tool result has status "success",
use the returned result to answer the user.

If the tool result has status "error",
inspect the error message and determine
whether the tool input can be corrected.

If you can correct the input,
call the tool again.

If the task is complete:

ANSWER: <final answer>

If another tool is required:

TOOL: <tool name>
INPUT: <tool input>
"""
                )

                # Continue Agent Loop

                continue

            # ----------------------------------
            # INVALID LLM RESPONSE
            # ----------------------------------

            messages.append(
                """
Your response format was invalid.

You MUST return exactly one of the
following formats.

For a final answer:

ANSWER: <answer>

For a tool call:

TOOL: <tool name>
INPUT: <tool input>

Do not return any other format.
"""
            )

        # ----------------------------------
        # Maximum Steps Reached
        # ----------------------------------

        return (
            "The Agent reached the maximum "
            "number of steps without producing "
            "a final answer."
        )