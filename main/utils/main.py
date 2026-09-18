import os
import importlib.util
import inspect
from langchain.agents import Tool

TOOLS_FOLDER = os.path.join(os.path.dirname(__file__), "tools")

def limit_output(func, max_chars=1000):
    """Wraps a function so its output is truncated to max_chars."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        text = str(result)
        if len(text) > max_chars:
            text = text[:max_chars] + "\n... [TRUNCATED] ..."
        return text
    return wrapper

def listoftools(max_chars=2000):
    tools = []

    for filename in os.listdir(TOOLS_FOLDER):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            file_path = os.path.join(TOOLS_FOLDER, filename)

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, func in inspect.getmembers(module, inspect.isfunction):
                tools.append(
                    Tool(
                        name=name,
                        func=limit_output(func, max_chars=max_chars),
                        description=inspect.getdoc(func) or f"Auto-discovered tool from {filename}"
                    )
                )

    return tools