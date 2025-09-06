from utils import get_club_by_email, \
                  get_club_by_name, \
                  get_competition_by_name, \
                  update_clubs_in_json, \
                  load_clubs, load_competitions \

import pytest
from unittest.mock import mock_open, patch
import json


# TESTS FILES MANAGEMENT
def test_load_clubs(clubs_data):
    mock_file = mock_open(read_data=json.dumps(clubs_data))
    with patch("builtins.open", mock_file):
        load_clubs()
    assert mock_file().read.called


def test_load_competitions(competitions_data_str):
    mock_file = mock_open(read_data=json.dumps(competitions_data_str))
    with patch("builtins.open", mock_file):
        load_competitions()
    assert mock_file().read.called


def test_update_clubs_in_json():
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        update_clubs_in_json([{"name": "Club1", "points": 10}])

    # Vérifiez que 'write' a été appelé au moins une fois
    assert mock_file().write.called


def test_update_competitions_in_json():
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        update_clubs_in_json([{"name": "competition1", "date": "2025-10-22 13:30:00", "numberOfPlaces": 10}])

    assert mock_file().write.called


# TESTS GETTERS
def test_email_found_returns_club(clubs_data):

    email_fourni = "email@club3.com"
    selected_club = get_club_by_email(clubs_data["clubs"], email_fourni)

    assert selected_club['email'] == "email@club3.com"


def test_email_not_found_raises_error(clubs_data):

    email_fourni = "email@club4.com"

    with pytest.raises(IndexError):
        get_club_by_email(clubs_data["clubs"], email_fourni)


def test_club_name_found_return_club(clubs_data):

    name_given = "Club2"
    selected_club = get_club_by_name(clubs_data["clubs"], name_given)

    assert selected_club['name'] == "Club2"


def test_club_name_not_found_raises_error(clubs_data):

    name_given = "Club10"

    with pytest.raises(IndexError):
        get_club_by_name(clubs_data["clubs"], name_given)


def test_competition_name_found_return_competition(competitions_data):

    name_given = "Competition1"
    selected_club = get_competition_by_name(
        competitions_data["competitions"],
        name_given
    )

    assert selected_club['name'] == "Competition1"


def test_competition_name_not_found_raises_error(competitions_data):

    name_given = "Competition10"

    with pytest.raises(IndexError):
        get_competition_by_name(competitions_data["competitions"], name_given)
