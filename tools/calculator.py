class CalculatorTool:

    name = "calculator"

    description = """
    Performs mathematical calculations.

    Use this tool when the user asks for arithmetic
    calculations such as addition, subtraction,
    multiplication, division, percentages, powers, etc.
    """

    @staticmethod
    def run(expression):

        try:
            result = eval(
                expression,
                {"__builtins__": {}},
                {}
            )

            return result

        except Exception as e:

            return f"Calculation error: {e}"