import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import app
import pytest


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# test intégrations
def test_email_not_valid(client):
    response = client.post('/showSummary', data={
        'email': 'clubconnnu@example.com'},
        follow_redirects=True)
    assert response.status_code == 200
    assert b"Email inconnu" in response.data


def test_email_valid(client):
    response = client.post('/showSummary', data={
        'email': 'admin@irontemple.com'},
        follow_redirects=True)
    assert response.status_code == 200
    assert b"Email inconnu" not in response.data

