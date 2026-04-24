from crewai import Agent, Task, Crew, Process
from langchain_community.chat_models import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
import numexpr

# Initialize local LLM
llm = ChatOllama(model="llama3", temperature=0.2)

# Define Tools
search_tool = DuckDuckGoSearchRun()
wiki_wrapper = WikipediaAPIWrapper()
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

@tool("Math Tool")
def math_tool(expression: str) -> str:
    """Useful for evaluating mathematical expressions. Input should be a valid mathematical expression string."""
    try:
        result = numexpr.evaluate(expression)
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
        llm=llm
    )

    # Agent 2: Calculator/Data Processor
    calculator = Agent(
        role='Data Processor & Mathematician',
        goal='Perform accurate mathematical calculations when requested.',
        backstory='You are a precise calculator. You use the Math Tool to evaluate equations and numeric expressions accurately.',
        verbose=True,
        allow_delegation=False,
        tools=[math_tool],
        llm=llm
    )

    # Agent 3: Summarizer / Final Answer
    writer = Agent(
        role='Senior Writer',
        goal='Synthesize the research and calculations into a clear, concise, and helpful final response.',
        backstory='You are an expert writer. You take the findings from the Researcher and Calculator and formulate a perfect response to the user.',
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    # Tasks
    task_research = Task(
        description=f'Analyze the query: "{query}". If it requires factual information or searching, use your tools to find it. If no research is needed, just state "No research needed".',
        expected_output='Factual information related to the query, or "No research needed".',
        agent=researcher
    )

    task_math = Task(
        description=f'Analyze the query: "{query}". If it contains mathematical expressions or requires calculation, use the Math Tool. If not, just state "No calculation needed".',
        expected_output='Calculated result, or "No calculation needed".',
        agent=calculator
    )

    task_write = Task(
        description=f'Combine the findings from the research and math tasks to provide a direct and final answer to the original query: "{query}". Make sure it is accurate and well-formatted.',
        expected_output='A clear, concise, and helpful final response directly addressing the user\'s query.',
        agent=writer
    )

    # Crew
    crew = Crew(
        agents=[researcher, calculator, writer],
        tasks=[task_research, task_math, task_write],
        process=Process.sequential,
        verbose=2
    )

    result = crew.kickoff()
    return result
