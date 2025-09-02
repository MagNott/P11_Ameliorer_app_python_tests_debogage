def get_club_by_email(p_l_dict_clubs, p_email_connexion):
    selected_club = [
        d_club
        for d_club in p_l_dict_clubs
        if d_club['email'] == p_email_connexion]
    return selected_club[0]
