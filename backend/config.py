"""
Centralized Configuration for Local Agent SLM.
You can easily swap out models here to scale vertically.
"""

# The Manager/Router model that orchestrates the agents and does general reasoning
MANAGER_MODEL = "ollama/llama3.2"

# The general Researcher model
RESEARCHER_MODEL = "ollama/llama3.2"

# The specialized Coding model
CODER_MODEL = "ollama/qwen2.5-coder"

# The specialized Math/Logic model
MATH_MODEL = "ollama/phi3.5"
