from llm.llm import LLM

from agent.prompts import SYSTEM_PROMPT

from tools.registry import ToolRegistry
from tools.calculator import CalculatorTool
from tools.csv_tool import CSVTool
from tools.web_search import WebSearchTool

from memory.memory_manager import MemoryManager


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

        # ----------------------------------
        # Initialize Conversation Memory
        # ----------------------------------

        self.memory = MemoryManager(
            max_messages=12
        )

    # ======================================
    # RUN AGENT
    # ======================================

    def run(self, question):

        # ----------------------------------
        # Build Tool Descriptions
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
        # Initialize Memory
        # ----------------------------------

        if not self.memory.get():

            self.memory.add(
                system_prompt
            )

        # ----------------------------------
        # Add User Question
        # ----------------------------------

        self.memory.add(
            f"User question:\n{question}"
        )

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
            # Build Current Prompt
            # ----------------------------------

            prompt = self.memory.get_context()

            # ----------------------------------
            # Ask LLM
            # ----------------------------------

            response = self.llm.generate(
                prompt
            )

            print("\nLLM Response:")
            print(response)

            # ----------------------------------
            # FINAL ANSWER
            # ----------------------------------

            if "ANSWER:" in response:

                answer = response.split(
                    "ANSWER:",
                    1
                )[1].strip()

                return answer

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
                # Validate Tool Name
                # ----------------------------------

                if not tool_name:

                    self.memory.add(
                        """
Your tool request did not contain
a valid tool name.

Return:

TOOL: <tool name>
INPUT: <JSON input>
"""
                    )

                    continue

                # ----------------------------------
                # Validate Tool Input
                # ----------------------------------

                if not tool_input:

                    self.memory.add(
                        """
Your tool request did not contain
valid tool input.

Return:

TOOL: <tool name>
INPUT: <JSON input>
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

                    self.memory.add(
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
                # Store Successful Tool Result
                # as an Important Fact
                # ----------------------------------

                if isinstance(result, dict):

                    if result.get("status") == "success":

                        self.memory.add_fact(
                            f"{tool_name}: {result}"
                        )

                # ----------------------------------
                # Add Tool Observation to Memory
                # ----------------------------------

                self.memory.add(
                    f"""
Tool: {tool_name}

Input:
{tool_input}

Tool Result:
{result}

IMPORTANT:

You are solving the ORIGINAL user question.

If the tool result has status "success":

Use the result to continue solving
the original question.

If the tool result has status "error":

1. Understand the error.
2. Do not blindly repeat the same failed
   tool call with the same input.
3. You may correct the input only if the
   correction is clearly supported by the
   original question or tool result.
4. Never silently replace the user's
   requested column, metric, entity,
   or condition.
5. If the requested information does not
   exist, provide a clear final answer.

Do NOT change the user's question simply
to produce an answer.

If the task is complete:

ANSWER: <final answer>

If another tool is required:

TOOL: <tool name>
INPUT: <JSON input>

Return ONLY one of these formats.
"""
                )

                # ----------------------------------
                # Continue Agent Loop
                # ----------------------------------

                continue

            # ----------------------------------
            # INVALID LLM RESPONSE
            # ----------------------------------

            self.memory.add(
                """
Your response format was invalid.

You MUST return exactly one of:

ANSWER: <final answer>

or:

TOOL: <tool name>
INPUT: <JSON input>

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


#                          USER
#                            │
#                            ▼
#                         AGENT
#                            │
#               ┌────────────┴────────────┐
#               │                         │
#               ▼                         ▼
#            MEMORY                     TOOLS
#               │                  ┌──────┼──────┐
#        ┌──────┴──────┐           │      │      │
#        │             │          CSV    Calc    Web
#    Recent          Facts
#   Messages
#        │             │
#        └──────┬──────┘
#               │
#               ▼
#              LLM
#               │
#        ┌──────┴──────┐
#        │             │
#       TOOL         ANSWER
#        │
#        ▼
#    Tool Result
#        │
#        ├── Recent Memory
#        │
#        └── Important Fact