from crewai import Agent, Task, Crew, Process
try:
    from crewai.tools import tool
except ImportError:
    from langchain_core.tools import tool

@tool("Math Tool")
def math_tool(expression: str) -> str:
    """Useful for evaluating mathematical expressions."""
    return "4"

try:
    researcher = Agent(
        role='Senior Research Analyst',
        goal='Uncover detailed and accurate information.',
        backstory='You are an expert researcher.',
        verbose=True,
        allow_delegation=False,
        tools=[math_tool],
        llm="ollama/llama3"
    )
    print("Agent initialized successfully!")
except Exception as e:
    print(f"Error: {e}")

