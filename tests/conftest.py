import pytest


@pytest.fixture
def clubs_data():
    club_list = {"clubs": [
        {
            "name": "Club1",
            "email": "email@club1.com",
            "points": "12"
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
            "date": "2025-11-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Competition2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]}

    return competitions_list
