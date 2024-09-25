import pytest
from main import app

# Fixture to create a test client for the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test for the index route
def test_index(client):
    """Test the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data  # Assuming the index page is HTML

# Test for the predict route
def test_predict(client):
    """Test the prediction is returned correctly."""
    # Simulating a POST request with form data
    response = client.post('/predict', data={
        'outlook': 'Sunny',
        'temperature': 'Hot',
        'humidity': 'High',
        'wind': 'Weak'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'prediction' in json_data
    assert json_data['prediction'] in ['Yes', 'No']  # Ensure prediction is one of the two classes
