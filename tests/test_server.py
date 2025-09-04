from server import app
import pytest
from unittest.mock import mock_open, patch


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_file_write():
    with patch("builtins.open", mock_open()) as mocked_file:
        yield mocked_file


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


def test_purchase_enough_points(
        client,
        mock_file_write,
        clubs_data,
        competitions_data
):
    with patch("server.loadClubs", return_value=clubs_data["clubs"]), \
         patch(
             "server.loadCompetitions",
             return_value=competitions_data["competitions"]):

        nom_competition = competitions_data["competitions"][0]["name"]
        nom_club = clubs_data["clubs"][0]["name"]
        response = client.post('/purchasePlaces', data={
            'competition': nom_competition,
            'club': nom_club,
            'places': '2'
            },
            follow_redirects=True)
        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data
        assert mock_file_write().write.called


def test_purchase_not_enough_points(
        client,
        mock_file_write,
        clubs_data,
        competitions_data):
    with patch("server.loadClubs", return_value=clubs_data["clubs"]), \
         patch(
             "server.loadCompetitions",
             return_value=competitions_data["competitions"]):

        nom_competition = competitions_data["competitions"][0]["name"]
        nom_club = clubs_data["clubs"][0]["name"]
        response = client.post('/purchasePlaces', data={
            'competition': nom_competition,
            'club': nom_club,
            'places': '99'
            },
            follow_redirects=True)
        assert response.status_code == 200
        assert b"Insufficient points to complete this reservation" in response.data
        assert not mock_file_write().write.called
