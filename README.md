# LocalAgent-SLM (Multi-Agent System)

![UI Preview](./ui_preview.png)

Build fully functional, offline AI agents that run entirely on your own hardware. This project leverages the new generation of compact, efficient Small Language Models (SLMs) to enable reasoning, planning, and task execution on standard laptops—eliminating API costs and ensuring total data privacy.

## Multi-LLM Agent Architecture
We utilize a **Hierarchical Multi-LLM setup**. Instead of using one "jack-of-all-trades" model, a **Supervisor Agent** evaluates your query and automatically assigns tasks to specialized agents running entirely different models.

```mermaid
flowchart TD
    A[User Prompt] --> B{Manager Agent llama3.2}
    
    subgraph Multi-Agent Topology
        B
        C[Researcher Agent llama3.2]
        D[Software Engineer qwen2.5-coder]
        E[Math & Logic Agent phi3.5]
    end
    
    B -->|Research Task| C
    B -->|Coding Task| D
    B -->|Math Task| E
    
    C -.->|Tools Output| B
    D -.->|Code Output| B
    E -.->|Math Result| B
    
    B --> F[Final Answer]
```

### The LLM Lineup
This vertical scaling is easily configurable in `backend/config.py`.
1. **Llama 3.2** - *Manager & Researcher*: Llama 3.2 is an incredibly fast, highly capable Small Language Model optimized for multi-lingual and agentic tasks. It's perfectly suited for orchestrating the crew and finding facts.
2. **Qwen 2.5 Coder** - *Software Engineer*: The state-of-the-art local coding model. It writes clean, efficient code far better than general-purpose SLMs.
3. **Phi-3.5** - *Mathematician*: Highly optimized for deep logic and mathematics.

## Prerequisites
1. **Python 3.10+**: Ensure you have a modern version of Python installed.
2. **Ollama**: You must install Ollama to run the models locally.
   - Download Ollama from [https://ollama.com/](https://ollama.com/)
   - Once installed, pull the models used in our topology:
     ```bash
     ollama run llama3.2
     ollama run qwen2.5-coder
     ollama run phi3.5
     ```
     *(Type `/bye` to exit the ollama prompt after downloading)*

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
1. The **Supervisor Agent (llama4-scout)** evaluates the query.
2. It assigns tasks to the specialized agents (Researcher, Coder, Calculator) using their respective tools.
3. The agents utilize their specialized local models to complete the work.
4. The Supervisor synthesizes their findings and provides the absolute best answer back to the UI!
