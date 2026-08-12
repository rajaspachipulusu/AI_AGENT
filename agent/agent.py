from llm.llm import LLM

from agent.prompts import SYSTEM_PROMPT

from tools.registry import ToolRegistry
from tools.calculator import CalculatorTool


class Agent:

    def __init__(self):

        self.llm = LLM()

        self.registry = ToolRegistry()

        self.registry.register(
            CalculatorTool
        )

    def run(self, question):

        tool_descriptions = (
            self.registry.describe_tools()
        )

        system_prompt = SYSTEM_PROMPT.format(
            tools=tool_descriptions
        )

        messages = [
            system_prompt,
            f"User question:\n{question}"
        ]

        max_steps = 5

        for step in range(max_steps):

            print(
                f"\n========== Agent Step "
                f"{step + 1} =========="
            )

            prompt = "\n\n".join(messages)

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

                # ------------------------------
                # Find Tool
                # ------------------------------

                tool = self.registry.get(
                    tool_name
                )

                if tool is None:

                    return (
                        f"Unknown tool requested: "
                        f"{tool_name}"
                    )

                print(
                    f"\nCalling Tool: {tool_name}"
                )

                print(
                    f"Tool Input: {tool_input}"
                )

                # ------------------------------
                # Execute Tool
                # ------------------------------

                result = tool.run(
                    tool_input
                )

                print(
                    f"Tool Result: {result}"
                )

                # ------------------------------
                # Add observation
                # ------------------------------

                messages.append(
                    f"""
Tool: {tool_name}

Input:
{tool_input}

Result:
{result}

Now decide what to do next.

If the task is complete:

ANSWER: <final answer>

If another tool is required:

TOOL: <tool name>
INPUT: <tool input>
"""
                )

                continue

            # ----------------------------------
            # INVALID RESPONSE
            # ----------------------------------

            messages.append(
                """
Your response format was invalid.

You MUST return exactly one of:

ANSWER: <answer>

or:

TOOL: <tool name>
INPUT: <tool input>
"""
            )

        return (
            "The Agent reached the maximum "
            "number of steps."
        )