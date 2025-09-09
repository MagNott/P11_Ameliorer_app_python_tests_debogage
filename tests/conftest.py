from datetime import datetime
import pytest
from unittest.mock import mock_open, patch
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_file_write():
    with patch("builtins.open", mock_open()) as mocked_file:
        yield mocked_file


@pytest.fixture
def patch_clubs_and_competitions(clubs_data, competitions_data):
    with patch("server.load_clubs", return_value=clubs_data["clubs"]), \
         patch("server.load_competitions", return_value=competitions_data["competitions"]):
        yield


@pytest.fixture
def clubs_data():
    club_list = {"clubs": [
        {
            "name": "Club1",
            "email": "email@club1.com",
            "points": "50"
        },
        {
            "name": "Club2",
            "email": "email@club2.com",
            "points": "4"
        },
        {
            "name": "Club3",
            "email": "email@club3.com",
            "points": "13"
        }
    ]}
    return club_list


@pytest.fixture
def competitions_data():
    competitions_list = {"competitions": [
        {
            "name": "Competition1",
            "date": datetime.strptime(
                "2999-11-27 10:00:00",
                "%Y-%m-%d %H:%M:%S"
            ),
            "numberOfPlaces": "25"
        },
        {
            "name": "Competition2",
            "date": datetime.strptime(
                "2020-10-22 13:30:00",
                "%Y-%m-%d %H:%M:%S"
            ),
            "numberOfPlaces": "13"
        }
    ]}

    return competitions_list


@pytest.fixture
def competitions_data_str():
    competitions_list = {"competitions": [
        {
            "name": "Competition1",
            "date": "2999-11-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Competition2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]}

    return competitions_list
