import json
import pandas as pd

from config import CSV_FILE


class CSVTool:

    name = "csv_analyzer"

    description = """
    Analyzes the employee CSV dataset.

    Input must be JSON.

    Supported actions:

    1. average
       Example:
       {"action": "average", "column": "Salary"}

    2. maximum
       Example:
       {"action": "maximum", "column": "Salary"}

    3. minimum
       Example:
       {"action": "minimum", "column": "Salary"}

    4. count
       Example:
       {"action": "count", "column": "Salary"}

    5. average_by_group
       Example:
       {
           "action": "average_by_group",
           "group_by": "Department",
           "column": "Salary"
       }

    Use this tool for questions about
    employees, salaries, departments,
    experience, counts, averages,
    minimums, maximums, and grouped analysis.
    """

    @staticmethod
    def run(tool_input):

        try:

            # ----------------------------------
            # Parse LLM input
            # ----------------------------------

            if isinstance(tool_input, str):

                data = json.loads(tool_input)

            else:

                data = tool_input

            action = data.get("action")
            column = data.get("column")
            group_by = data.get("group_by")

            # ----------------------------------
            # Load CSV
            # ----------------------------------

            df = pd.read_csv(CSV_FILE)

            # ----------------------------------
            # Resolve column names
            # ----------------------------------

            def find_column(column_name):

                if not column_name:
                    return None

                for df_column in df.columns:

                    if (
                        df_column.lower()
                        == column_name.lower()
                    ):
                        return df_column

                return None

            actual_column = find_column(column)

            actual_group_by = find_column(group_by)

            # ----------------------------------
            # Average
            # ----------------------------------

            if action == "average":

                if actual_column is None:

                    return {
                        "status": "error",
                        "message": (
                            f"Column '{column}' "
                            "not found."
                        ),
                        "available_columns": list(
                            df.columns
                        )
                    }

                result = df[actual_column].mean()

                return {
                    "status": "success",
                    "action": action,
                    "column": actual_column,
                    "result": float(result)
                }

            # ----------------------------------
            # Maximum
            # ----------------------------------

            if action == "maximum":

                if actual_column is None:

                    return {
                        "status": "error",
                        "message": (
                            f"Column '{column}' "
                            "not found."
                        ),
                        "available_columns": list(
                            df.columns
                        )
                    }

                result = df[actual_column].max()

                return {
                    "status": "success",
                    "action": action,
                    "column": actual_column,
                    "result": result
                }

            # ----------------------------------
            # Minimum
            # ----------------------------------

            if action == "minimum":

                if actual_column is None:

                    return {
                        "status": "error",
                        "message": (
                            f"Column '{column}' "
                            "not found."
                        ),
                        "available_columns": list(
                            df.columns
                        )
                    }

                result = df[actual_column].min()

                return {
                    "status": "success",
                    "action": action,
                    "column": actual_column,
                    "result": result
                }

            # ----------------------------------
            # Count
            # ----------------------------------

            if action == "count":

                if actual_column is None:

                    return {
                        "status": "error",
                        "message": (
                            f"Column '{column}' "
                            "not found."
                        ),
                        "available_columns": list(
                            df.columns
                        )
                    }

                result = df[actual_column].count()

                return {
                    "status": "success",
                    "action": action,
                    "column": actual_column,
                    "result": int(result)
                }

            # ----------------------------------
            # Average By Group
            # ----------------------------------

            if action == "average_by_group":

                if actual_group_by is None:

                    return {
                        "status": "error",
                        "message": (
                            f"Group column "
                            f"'{group_by}' not found."
                        ),
                        "available_columns": list(
                            df.columns
                        )
                    }

                if actual_column is None:

                    return {
                        "status": "error",
                        "message": (
                            f"Column '{column}' "
                            "not found."
                        ),
                        "available_columns": list(
                            df.columns
                        )
                    }

                result = (
                    df.groupby(actual_group_by)[
                        actual_column
                    ]
                    .mean()
                    .round(2)
                    .to_dict()
                )

                return {
                    "status": "success",
                    "action": action,
                    "group_by": actual_group_by,
                    "column": actual_column,
                    "result": result
                }

            # ----------------------------------
            # Unsupported Action
            # ----------------------------------

            return {
                "status": "error",
                "message": (
                    f"Unsupported action: {action}"
                ),
                "supported_actions": [
                    "average",
                    "maximum",
                    "minimum",
                    "count",
                    "average_by_group"
                ]
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }