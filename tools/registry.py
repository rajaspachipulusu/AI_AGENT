class ToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(self, tool):

        self.tools[tool.name] = tool

    def get(self, name):

        return self.tools.get(name)

    def get_all(self):

        return self.tools

    def describe_tools(self):

        descriptions = []

        for tool in self.tools.values():

            descriptions.append(
                f"""
Tool: {tool.name}

Description:
{tool.description}
"""
            )

        return "\n".join(descriptions)