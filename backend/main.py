import os
import signal
import sys
import urllib.request
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.agents import run_crew
from backend.config import CODER_MODEL, MATH_MODEL, MANAGER_MODEL

# Forcefully kill the server on Ctrl+C, skipping thread graceful shutdown
def force_exit(signum, frame):
    print("\nForcefully exiting the server...")
    os._exit(1)

signal.signal(signal.SIGINT, force_exit)
signal.signal(signal.SIGTERM, force_exit)

def fast_ollama_call(model_name: str, prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    clean_model = model_name.replace("ollama/", "")
    payload = {
        "model": clean_model,
        "prompt": prompt,
        "stream": False
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "Error: No response from Ollama.")
    except Exception as e:
        return f"Ollama connection error: {e}"

app = FastAPI(title="Local SLM Multi-Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open(os.path.join(frontend_dir, "index.html"), "r") as f:
        return f.read()

FAST_RESPONSES = {
    "hi": "Hello! I am your local AI team. How can we help you today?",
    "hello": "Hi there! What can our agents do for you?",
    "hey": "Hey! Ready to research, code, or calculate. What's up?",
    "who are you": "I am a local Multi-Agent SLM system, featuring specialized Researcher, Coder, and Math agents!",
    "who are you?": "I am a local Multi-Agent SLM system, featuring specialized Researcher, Coder, and Math agents!",
    "how are you": "All local systems are running optimally! How can we assist?",
    "how are you?": "All local systems are running optimally! How can we assist?"
}

def fast_auto_router(query: str) -> str:
    cleaned = query.lower()
    if any(kw in cleaned for kw in ["code", "script", "python", "javascript", "html", "css", "bug", "error", "function"]):
        return fast_ollama_call(CODER_MODEL, f"You are an expert coder. Please fulfill this request: {query}")
    elif any(kw in cleaned for kw in ["calculate", "math", "solve", "equation"]) or any(char in cleaned for char in ["+", "-", "*", "/"]):
        return fast_ollama_call(MATH_MODEL, f"You are an expert mathematician. Solve this: {query}")
    else:
        return fast_ollama_call(MANAGER_MODEL, query)

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        cleaned_query = request.query.lower().strip()
        stripped_query = cleaned_query.strip("!?.,")
        
        # 1. FAST BYPASS: Instantly return answers to simple greetings
        if stripped_query in FAST_RESPONSES:
            return {"response": FAST_RESPONSES[stripped_query]}

        # 2. SLASH COMMAND ROUTING
        if cleaned_query.startswith("/code"):
            prompt = request.query[5:].strip()
            return {"response": fast_ollama_call(CODER_MODEL, prompt)}
            
        if cleaned_query.startswith("/math"):
            prompt = request.query[5:].strip()
            return {"response": fast_ollama_call(MATH_MODEL, prompt)}

        # 3. DEEP RESEARCH ROUTE: Run the full multi-agent CrewAI system
        if cleaned_query.startswith("/deep"):
            prompt = request.query[5:].strip()
            response = run_crew(prompt)
            return {"response": str(response)}

        # 4. DEFAULT ROUTE: Blazing fast auto-router instead of slow CrewAI
        res = fast_auto_router(request.query)
        return {"response": res}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
