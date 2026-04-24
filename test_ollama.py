from backend.main import fast_ollama_call
print("Result:")
print(fast_ollama_call("ollama/qwen2.5-coder", "print hello world"))
