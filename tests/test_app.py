
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Guinness' in response.data  # Adjust if your home.html has a different keyword

def test_submit_rating_missing_data(client):
    response = client.post('/api/ratings', json={})
    assert response.status_code == 400
    assert b'Missing place or rating' in response.data

def test_get_ratings(client):
    response = client.get('/api/ratings')
    assert response.status_code == 200
