from unittest.mock import mock_open, patch


def test_user_can_view_club_points_after_login(
        client,
        patch_clubs_and_competitions):

    response_login = client.post('/showSummary', data={
        "email": "email@club1.com"},
        follow_redirects=True)

    assert response_login.status_code == 200
    assert b"Welcome" in response_login.data

    response_clubs = client.get("/showclubs")

    assert response_clubs.status_code == 200
    assert b"Club name" in response_clubs.data
    assert b"email@club1.com" in response_clubs.data


def test_secretary_can_book_competition_and_view_points(
        client,
        patch_clubs_and_competitions,
        clubs_data,
        competitions_data):

    response_login = client.post('/showSummary', data={
        "email": "email@club1.com"},
        follow_redirects=True)

    assert response_login.status_code == 200
    assert b"Welcome" in response_login.data

    nom_competition = competitions_data["competitions"][0]["name"]
    nom_club = clubs_data["clubs"][0]["name"]

    response_booking_page = client.get(f'/book/{nom_competition}/{nom_club}')
    assert response_booking_page.status_code == 200
    assert b"Places available" in response_booking_page.data

    with patch("builtins.open", mock_open()) as f:
        response_purchase_places = client.post('/purchasePlaces', data={
            'competition': nom_competition,
            'club': nom_club,
            'places': '2'
            },
            follow_redirects=True)
        competition = next(
            competition
            for competition in competitions_data["competitions"]
            if competition["name"] == nom_competition)
        assert int(competition['numberOfPlaces']) == (25 - 2)
        assert response_purchase_places.status_code == 200
        assert b"Great-booking complete!" in response_purchase_places.data
        assert f().write.called

    response_clubs = client.get("/showclubs")

    assert response_clubs.status_code == 200
    assert b"Club name" in response_clubs.data
    assert b"email@club1.com" in response_clubs.data

    response_logout = client.get('/logout', follow_redirects=True)

    assert response_logout.status_code == 200
    assert b"Welcome" in response_logout.data

    # LE TEST DE LA GALERE
