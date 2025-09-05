import json


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


def update_clubs_in_json(p_l_dict_clubs):
    with open("clubs.json", "w") as f:
        json.dump({"clubs": p_l_dict_clubs}, f, indent=4)


def update_competitions_in_json(p_l_dict_competitions):
    with open("competitions.json", "w") as f:
        json.dump({"competitions": p_l_dict_competitions}, f, indent=4)
