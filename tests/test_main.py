from fastapi.testclient import TestClient
from unittest.mock import patch
import os

from backend.main import app

client = TestClient(app)

def test_read_root():
    """Test that the frontend HTML is served properly."""
    # Ensure index.html exists where expected for the test
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
    assert os.path.exists(os.path.join(frontend_dir, "index.html")), "index.html must exist"
    
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Local AI Agent" in response.text

@patch("backend.main.run_crew")
def test_chat_endpoint_success(mock_run_crew):
    """Test the chat endpoint successfully returns a simulated agent response."""
    # Mock the crewai response so we don't actually call Ollama during the test
    mock_run_crew.return_value = "This is a mocked agent response."
    
    payload = {"query": "What is 2 + 2?"}
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"response": "This is a mocked agent response."}
    mock_run_crew.assert_called_once_with("What is 2 + 2?")

@patch("backend.main.run_crew")
def test_chat_endpoint_error_handling(mock_run_crew):
    """Test that errors from the agent engine are handled gracefully."""
    mock_run_crew.side_effect = Exception("Ollama connection failed.")
    
    payload = {"query": "Perform an error task."}
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    assert response.json() == {"error": "Ollama connection failed."}
