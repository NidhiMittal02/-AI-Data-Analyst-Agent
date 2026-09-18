import os
import importlib.util
import inspect

from langchain.agents import Tool


TOOLS_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "tools"
)


# ============================================================
# LIMIT TOOL OUTPUT
# ============================================================

def limit_output(
    func,
    max_chars=1000
):
    """
    Wrap a function so its output is truncated
    to max_chars.
    """

    def wrapper(
        *args,
        **kwargs
    ):
        result = func(
            *args,
            **kwargs
        )

        text = str(result)

        if len(text) > max_chars:
            text = (
                text[:max_chars]
                + "\n... [TRUNCATED] ..."
            )

        return text

    return wrapper


# ============================================================
# LOAD ANALYSIS TOOLS
# ============================================================

def listoftools(
    max_chars=2000
):
    """
    Load only the analysis tools required
    by the current data-analysis agent.
    """

    tools = []

    allowed_files = [
        "analysis_tools.py"
    ]

    for filename in allowed_files:

        file_path = os.path.join(
            TOOLS_FOLDER,
            filename
        )

        if not os.path.exists(
            file_path
        ):
            continue

        module_name = filename[:-3]

        spec = (
            importlib.util
            .spec_from_file_location(
                module_name,
                file_path
            )
        )

        module = (
            importlib.util
            .module_from_spec(
                spec
            )
        )

        spec.loader.exec_module(
            module
        )

        for name, func in inspect.getmembers(
            module,
            inspect.isfunction
        ):

            tools.append(
                Tool(
                    name=name,
                    func=limit_output(
                        func,
                        max_chars=max_chars
                    ),
                    description=(
                        inspect.getdoc(func)
                        or
                        f"Analysis tool from {filename}"
                    )
                )
            )

    return tools