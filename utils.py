import json
from datetime import datetime
from copy import deepcopy
import os


CLUBS_FILE = "clubs_test.json" if os.getenv("FLASK_ENV") == "performance" else "clubs.json"
COMPETITIONS_FILE = "comptetitions_test.json" if os.getenv("FLASK_ENV") == "performance" else "comptetitions.json"


# FILES MANAGEMENTS
def load_clubs():
    with open(CLUBS_FILE) as c:
        listOfClubs = json.load(c)['clubs']
    return listOfClubs


def load_competitions():
    with open(COMPETITIONS_FILE) as competitions:
        listOfCompetitions = json.load(competitions)['competitions']
    for competition in listOfCompetitions:
        object_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
        competition["date"] = object_date

    return listOfCompetitions


def update_clubs_in_json(p_l_dict_clubs):
    with open(CLUBS_FILE, "w") as f:
        json.dump({"clubs": p_l_dict_clubs}, f, indent=4)


def update_competitions_in_json(p_l_dict_competitions):
    with open(COMPETITIONS_FILE, "w") as f:
        copy_p_l_dict_competitions = deepcopy(p_l_dict_competitions)
        for competition in copy_p_l_dict_competitions:
            object_date = datetime.strftime(competition["date"], "%Y-%m-%d %H:%M:%S")
            competition["date"] = object_date
        json.dump({"competitions": copy_p_l_dict_competitions}, f, indent=4)


# GETTERS
def get_club_by_email(p_l_dict_clubs, p_email_connexion):
    selected_club = [
        d_club
        for d_club in p_l_dict_clubs
        if d_club['email'] == p_email_connexion
    ]

    return selected_club[0]


def get_club_by_name(p_l_dict_clubs, p_name_club):
    selected_club = [
        club
        for club in p_l_dict_clubs
        if club['name'] == p_name_club
    ]
    return selected_club[0]


def get_competition_by_name(p_l_dict_competitions, p_name_competition):
    selected_competition = [
        competition
        for competition in p_l_dict_competitions
        if competition['name'] == p_name_competition
    ]
    return selected_competition[0]
