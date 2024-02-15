import pytest
from app import app as flask_app  # Import your Flask app
import os

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Setup: create a temporary database, configure the app for testing, etc.
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_index_page(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"index.html content" in response.data  # Check for expected content

def test_send_message(client, monkeypatch):
    """Test the send_message route."""
    # Example of patching the OpenAI API call to return a predefined response
    def mock_chat(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': 'Mocked response'})})]
        return MockResponse()
    
    monkeypatch.setattr("openai.OpenAI.chat.completions.create", mock_chat)

    response = client.post('/send_message', json={'message': 'Hello, world!'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'Mocked response' in data['message']
