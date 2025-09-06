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


def test_purchase_club_has_enough_points(
        client,
        mock_file_write,
        clubs_data,
        competitions_data
):
    with patch("server.load_clubs", return_value=clubs_data["clubs"]), \
         patch(
             "server.load_competitions",
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


def test_purchase_club_has_not_enough_points(
        client,
        mock_file_write,
        clubs_data,
        competitions_data):
    with patch("server.load_clubs", return_value=clubs_data["clubs"]), \
         patch(
             "server.load_competitions",
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


def test_purchase_more_than_12_places_should_fail(
        client,
        mock_file_write,
        clubs_data,
        competitions_data):
    with patch("server.load_clubs", return_value=clubs_data["clubs"]), \
         patch(
             "server.load_competitions",
             return_value=competitions_data["competitions"]):

        original_places = competitions_data["competitions"][0]["numberOfPlaces"]
        nom_competition = competitions_data["competitions"][0]["name"]
        nom_club = clubs_data["clubs"][0]["name"]
        response = client.post('/purchasePlaces', data={
            'competition': nom_competition,
            'club': nom_club,
            'places': '13'
            },
            follow_redirects=True)

        assert response.status_code == 200
        assert b"One club cannot book more than 12 places for a single competition" in response.data
        assert not mock_file_write().write.called
        assert competitions_data["competitions"][0]["numberOfPlaces"] == original_places


def test_purchase_12_or_less_places_should_succeed(
        client,
        mock_file_write,
        clubs_data,
        competitions_data):
    with patch("server.load_clubs", return_value=clubs_data["clubs"]), \
         patch(
             "server.load_competitions",
             return_value=competitions_data["competitions"]):

        original_places = competitions_data["competitions"][0]["numberOfPlaces"]
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
        assert competitions_data["competitions"][0]["numberOfPlaces"] != original_places


def test_book_competition_when_future_date(
        client,
        mock_file_write,
        clubs_data,
        competitions_data):

    with patch("server.load_clubs", return_value=clubs_data["clubs"]), \
         patch(
             "server.load_competitions",
             return_value=competitions_data["competitions"]):

        response = client.get('/book/Competition1/Club2')

        assert response.status_code == 200
        assert b"" in response.data
        assert not mock_file_write().write.called


def test_book_competition_when_passed_date(
        client,
        mock_file_write,
        clubs_data,
        competitions_data):

    with patch("server.load_clubs", return_value=clubs_data["clubs"]), \
         patch(
            "server.load_competitions",
            return_value=competitions_data["competitions"]):

        response = client.get('/book/Competition2/Club2')

        assert response.status_code == 200
        assert b"must be superior or equal" in response.data
        assert not mock_file_write().write.called
