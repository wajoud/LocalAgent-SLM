try:
    from crewai.tools import tool
    print("crewai.tools imported")
except ImportError:
    from langchain_core.tools import tool
    print("langchain_core.tools imported")
