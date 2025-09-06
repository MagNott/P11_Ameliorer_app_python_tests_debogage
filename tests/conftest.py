from datetime import datetime
import pytest


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
