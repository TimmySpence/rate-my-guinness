import sys
import os
import pytest
from flask import Flask
from flask_cors import CORS

# Ensure test mode before importing app
os.environ['FLASK_ENV'] = 'testing'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db

# Configure app for testing
TESTING = os.environ.get("TESTING") == "1"

app = Flask(__name__)
CORS(app)

if TESTING:
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # ...existing Postgres config...
    pass

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Create tables for each test run
    with app.app_context():
        db.create_all()
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
