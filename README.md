# LocalAgent-SLM (Multi-Agent System)

Build fully functional, offline AI agents that run entirely on your own hardware. This project leverages the new generation of compact, efficient Small Language Models (SLMs) to enable reasoning, planning, and task execution on standard laptops—eliminating API costs and ensuring total data privacy.

## Features
- **Multi-Agent System**: Utilizes `CrewAI` with 3 specialized agents (Researcher, Mathematician, Writer) working together.
- **Local Small Language Models (SLM)**: Powered by `Ollama` running `llama3` locally. Completely free and offline.
- **Tools**: Includes DuckDuckGo Search, Wikipedia, and a Math Tool to extend the capabilities of the SLMs.
- **FastAPI Backend**: A lightweight, fast backend for interacting with the agents.
- **Premium Frontend UI**: A beautiful, modern chat interface utilizing glassmorphism and smooth animations.

## Prerequisites
1. **Python 3.10+**: Ensure you have a modern version of Python installed.
2. **Ollama**: You must install Ollama to run the models locally.
   - Download Ollama from [https://ollama.com/](https://ollama.com/)
   - Once installed, open your terminal and pull the Llama 3 model by running:
     ```bash
     ollama run llama3
     ```
     *(You can exit the ollama prompt once it downloads by typing `/bye`)*

## Setup Instructions

1. **Install Python Dependencies**:
   Open a terminal in the project root directory and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   Start the FastAPI server by running:
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Open the UI**:
   Open your web browser and navigate to:
   [http://localhost:8000](http://localhost:8000)

## How it Works
When you send a message through the UI, it goes to the FastAPI backend. The backend kicks off a `CrewAI` process:
1. The **Researcher Agent** checks if web search or Wikipedia is needed.
2. The **Calculator Agent** checks if any math needs solving.
3. The **Writer Agent** synthesizes the findings and provides the final answer back to the UI.
All reasoning happens locally on your machine via the `llama3` model hosted in Ollama!
