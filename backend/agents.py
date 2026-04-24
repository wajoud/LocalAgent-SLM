from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from typing import Any
import numexpr
from backend.config import MANAGER_MODEL, CODER_MODEL, MATH_MODEL, RESEARCHER_MODEL

# Helper to fix Ollama's nested dictionary tool arguments
def parse_query(q: Any) -> str:
    if isinstance(q, dict):
        # Sometimes Ollama passes {"type": "string", "value": "actual query"}
        return q.get("value", str(q))
    return str(q)

# Define Tools via the wrapper to ensure Pydantic v2 compatibility
@tool("Search Tool")
def search_tool(query: Any) -> str:
    """Useful for searching the internet."""
    from langchain_community.tools import DuckDuckGoSearchRun
    return DuckDuckGoSearchRun().run(parse_query(query))

@tool("Wiki Tool")
def wiki_tool(query: Any) -> str:
    """Useful for searching wikipedia."""
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    return WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()).run(parse_query(query))

@tool("Math Tool")
def math_tool(expression: Any) -> str:
    """Useful for evaluating mathematical expressions. Input should be a valid mathematical expression string."""
    try:
        result = numexpr.evaluate(parse_query(expression))
        return str(result)
    except Exception as e:
        return f"Error evaluating math expression: {e}"

def run_crew(query: str):
    # Agent 1: Researcher
    researcher = Agent(
        role='Senior Research Analyst',
        goal='Uncover detailed and accurate information using available tools like web search and wikipedia.',
        backstory='You are an expert researcher. You analyze user queries and find the most accurate facts and data.',
        verbose=True,
        allow_delegation=False,
        tools=[search_tool, wiki_tool],
        llm=RESEARCHER_MODEL
    )

    # Agent 2: Calculator/Data Processor
    calculator = Agent(
        role='Data Processor & Mathematician',
        goal='Perform accurate mathematical calculations when requested.',
        backstory='You are a precise calculator. You use the Math Tool to evaluate equations and numeric expressions accurately.',
        verbose=True,
        allow_delegation=False,
        tools=[math_tool],
        llm=MATH_MODEL
    )

    # Agent 3: Software Engineer
    coder = Agent(
        role='Senior Software Engineer',
        goal='Write clean, efficient, and well-documented code.',
        backstory='You are an expert programmer. When the user asks for code, you provide robust software solutions.',
        verbose=True,
        allow_delegation=False,
        llm=CODER_MODEL
    )

    # Tasks
    task_research = Task(
        description=f'Research anything related to this query if fact-checking or context is needed: "{query}".',
        expected_output='Factual information from the web or wikipedia.',
        agent=researcher
    )

    task_math = Task(
        description=f'Solve any mathematical or logical parts of this query: "{query}".',
        expected_output='Math results.',
        agent=calculator
    )

    task_code = Task(
        description=f'Write any code or programming scripts required by this query: "{query}".',
        expected_output='Clean, functional code.',
        agent=coder
    )

    # Crew - Using Hierarchical process so the Manager Agent handles routing!
    crew = Crew(
        agents=[researcher, calculator, coder],
        tasks=[task_research, task_math, task_code],
        process=Process.hierarchical,
        manager_llm=MANAGER_MODEL,
        verbose=True
    )

    result = crew.kickoff()
    return result
