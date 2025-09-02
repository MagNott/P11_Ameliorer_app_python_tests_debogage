from utils import get_club_by_email
import pytest


def test_email_found_returns_club():

    club_list = {"clubs":[
        {
            "name": "Club1",
            "email": "email@club1.com",
            "points": "0"
        },
        {
            "name": "Club2",
            "email": "email@club2.com",
            "points": "0"
        },
        {   "name": "Club3",
            "email": "email@club3.com",
            "points": "0"
        }
    ]}
    email_fourni = "email@club3.com"
    selected_club = get_club_by_email(club_list["clubs"], email_fourni)

    assert selected_club['email'] == "email@club3.com"


def test_email_not_found_raises_error():

    club_list = {"clubs":[
        {
            "name": "Club1",
            "email": "email@club1.com",
            "points": "0"
        },
        {
            "name": "Club2",
            "email": "email@club2.com",
            "points": "0"
        },
        {   "name": "Club3",
            "email": "email@club3.com",
            "points": "0"
        }
    ]}
    email_fourni = "email@club4.com"

    with pytest.raises(IndexError):
        get_club_by_email(club_list["clubs"], email_fourni)
