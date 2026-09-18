import os

from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory

if 'VERCEL' in os.environ:
    from main.llm import AIPipeLLM
    from main.utils.main import listoftools
else:
    from llm import AIPipeLLM
    from utils.main import listoftools


# ---------------------------------------
# Language model used by fallback agent
# ---------------------------------------

llm = AIPipeLLM()


# ---------------------------------------
# Basic safety restrictions
# ---------------------------------------

FORBIDDEN = [
    "shutil",
    "os",
    "subprocess",
    "open(",
    "rm",
    "rmtree",
    "remove",
    "unlink",
    "sys.exit",
    "exit("
]


def safe_python_executor(code: str):
    """
    Execute Python code for data analysis while
    blocking common file/system-control operations.
    """

    if any(word in code for word in FORBIDDEN):

        return (
            "Your code contains unsafe operations. "
            "Do not use file deletion, OS commands, "
            "or subprocess operations."
        )

    return PythonREPLTool().run(code)


# ---------------------------------------
# Safe Python tool
# ---------------------------------------

safe_tool = Tool(
    name="Safe Python Executor",
    func=safe_python_executor,
    description=(
        "Executes Python code for data analysis. "
        "Use it for calculations and data processing. "
        "Do not perform file deletion, operating-system "
        "commands, subprocess operations, or other unsafe actions."
    )
)


# ---------------------------------------
# Automatically discover analysis tools
# ---------------------------------------

analysis_tools = listoftools()


# ---------------------------------------
# Combine all tools
# ---------------------------------------

tools = [
    safe_tool
] + analysis_tools


# ---------------------------------------
# Agent instructions
# ---------------------------------------

system_prompt = """
You are a reliable Python data analyst.

Your job is to analyze the currently uploaded dataset accurately.

IMPORTANT RULES:

1. Use the available Pandas analysis tools whenever possible
   for numerical calculations.

2. Do not manually calculate totals, averages, percentages,
   minimums, maximums, or grouped results when an analysis
   tool can perform the calculation.

3. Use the following types of analysis tools when appropriate:
   - calculate_total
   - calculate_average
   - calculate_minimum
   - calculate_maximum
   - calculate_row_count
   - calculate_unique_count
   - calculate_group_sum
   - calculate_group_average
   - get_top_n
   - calculate_percentage_of_total

4. Use the actual uploaded dataset for calculations.

5. Never invent data or numerical results.

6. Never use:
   - file deletion
   - operating-system commands
   - subprocess
   - shutil
   - rm
   - rmtree
   - remove
   - unlink
   - sys.exit
   - exit

7. Do not save files to disk unless explicitly required
   by a future feature.

8. Clean and inspect the data before making conclusions.

9. Return only the answer requested by the user.
"""


# ---------------------------------------
# Create LangChain agent
# ---------------------------------------

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={
        "system_message": system_prompt
    },
    memory=ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
)


# ---------------------------------------
# Fallback analysis function
# ---------------------------------------

def ask_agent(message):
    """
    Send a data-analysis request to the fallback
    LangChain agent.
    """

    prompt = (
        message
        + """

Respond with only the final answer.

Use the analysis tools whenever a calculation
is required.

Make sure numerical answers are calculated
from the uploaded dataset and are accurate.

Do not invent values.
"""
    )

    return agent.run(prompt)


# ---------------------------------------
# Direct testing
# ---------------------------------------

if __name__ == '__main__':

    test_file = os.path.join(
        os.path.dirname(__file__),
        "test_cases",
        "test_question.txt"
    )

    with open(test_file, "r", encoding="utf-8") as f:
        question = f.read()

    result = agent.run(
        question
        + """

Respond with only the final answer.
Use the available analysis tools for calculations.
"""
    )

    print()
    print(result)