from unittest.mock import mock_open, patch


def test_user_can_view_club_points_after_login(
        client,
        patch_clubs_and_competitions
):

    response_login = client.post(
        "/showSummary",
        data={"email": "email@club1.com"},
        follow_redirects=True
    )

    assert response_login.status_code == 200
    assert b"Welcome" in response_login.data

    response_clubs = client.get("/showclubs")

    assert response_clubs.status_code == 200
    assert b"Club name" in response_clubs.data
    assert b"email@club1.com" in response_clubs.data


def test_secretary_can_book_competition_and_view_points(
    client, patch_clubs_and_competitions, clubs_data, competitions_data
):
    """
    Functional test simulating a full user journey:
    - Correct login
    - Books successfully
    - Views club points
    - Logs out
    """

    response_login = client.post(
        "/showSummary",
        data={"email": "email@club1.com"},
        follow_redirects=True
    )

    assert response_login.status_code == 200
    assert b"Welcome" in response_login.data

    nom_competition = competitions_data["competitions"][0]["name"]
    nom_club = clubs_data["clubs"][0]["name"]

    response_booking_page = client.get(f"/book/{nom_competition}/{nom_club}")
    assert response_booking_page.status_code == 200
    assert b"Places available" in response_booking_page.data

    with patch("builtins.open", mock_open()) as f:
        response_purchase_places = client.post(
            "/purchasePlaces",
            data={
                "competition": nom_competition,
                "club": nom_club,
                "places": "2"},
            follow_redirects=True,
        )
        competition = next(
            competition
            for competition in competitions_data["competitions"]
            if competition["name"] == nom_competition
        )
        assert int(competition["numberOfPlaces"]) == (25 - 2)
        assert response_purchase_places.status_code == 200
        assert b"Great-booking complete!" in response_purchase_places.data
        assert f().write.called

    response_clubs = client.get("/showclubs")

    assert response_clubs.status_code == 200
    assert b"Club name" in response_clubs.data
    assert b"email@club1.com" in response_clubs.data

    response_logout = client.get("/logout", follow_redirects=True)

    assert response_logout.status_code == 200
    assert b"Welcome" in response_logout.data


def test_full_booking_workflow_with_invalid_scenarios(
    client, patch_clubs_and_competitions, clubs_data, competitions_data
):
    """
    Functional test simulating a full user journey:
    - Wrong login
    - Correct login
    - Tries to book too many places
    - Tries without enough points
    - Books twice successfully
    - Tries again when no places are left
    - Logs out
    """

    # SAD PATH wrong email
    response_login = client.post(
        "/showSummary",
        data={"email": "wrongemail@club1.com"},
        follow_redirects=True
    )

    assert response_login.status_code == 200
    assert b"Email inconnu" in response_login.data

    # HAPPY PATH
    response_login = client.post(
        "/showSummary",
        data={"email": "email@club1.com"},
        follow_redirects=True
    )

    assert response_login.status_code == 200
    assert b"Welcome" in response_login.data

    nom_competition = competitions_data["competitions"][0]["name"]
    nom_club = clubs_data["clubs"][0]["name"]

    # SAD PATH competition not found
    response_booking_page = client.get(
        "/book/fake_competition/Club1", follow_redirects=True
    )
    assert response_booking_page.status_code == 200
    msg = b"Club or Competition cannot be found, please log in again !"
    assert msg in response_booking_page.data

    # HAPPY PATH
    response_booking_page = client.get(f"/book/{nom_competition}/{nom_club}")
    assert response_booking_page.status_code == 200
    assert b"Places available" in response_booking_page.data

    # SAD PATH book more than 12 places
    with patch("builtins.open", mock_open()) as f:
        response_purchase_places = client.post(
            "/purchasePlaces",
            data={
                "competition": nom_competition,
                "club": nom_club,
                "places": "14"},
            follow_redirects=True,
        )
        competition = next(
            competition
            for competition in competitions_data["competitions"]
            if competition["name"] == nom_competition
        )
        assert response_purchase_places.status_code == 200
        msg = b"One club cannot book more than 12 places for a competition"
        assert msg in response_purchase_places.data

    # SAD PATH club has not enough points
    nom_club_with_not_enough_points = clubs_data["clubs"][1]["name"]
    with patch("builtins.open", mock_open()) as f:
        response_purchase_places = client.post(
            "/purchasePlaces",
            data={
                "competition": nom_competition,
                "club": nom_club_with_not_enough_points,
                "places": "5",
            },
            follow_redirects=True,
        )
        competition = next(
            competition
            for competition in competitions_data["competitions"]
            if competition["name"] == nom_competition
        )
        assert response_purchase_places.status_code == 200
        msg = b"Insufficient points to complete this reservation"
        assert msg in response_purchase_places.data

    # HAPPY PATH
    with patch("builtins.open", mock_open()) as f:
        response_purchase_places = client.post(
            "/purchasePlaces",
            data={"competition": nom_competition,
                  "club": nom_club,
                  "places": "10"},
            follow_redirects=True,
        )
        competition = next(
            competition
            for competition in competitions_data["competitions"]
            if competition["name"] == nom_competition
        )
        assert int(competition["numberOfPlaces"]) == (25 - 10)
        assert response_purchase_places.status_code == 200
        assert b"Great-booking complete!" in response_purchase_places.data
        assert f().write.called

    # HAPPY PATH
    with patch("builtins.open", mock_open()) as f:
        response_purchase_places = client.post(
            "/purchasePlaces",
            data={
                "competition": nom_competition,
                "club": nom_club,
                "places": "10"},
            follow_redirects=True,
        )
        competition = next(
            competition
            for competition in competitions_data["competitions"]
            if competition["name"] == nom_competition
        )
        assert int(competition["numberOfPlaces"]) == (15 - 10)
        assert response_purchase_places.status_code == 200
        assert b"Great-booking complete!" in response_purchase_places.data
        assert f().write.called

    # SAD PATH try to buy more places than left
    with patch("builtins.open", mock_open()) as f:
        response_purchase_places = client.post(
            "/purchasePlaces",
            data={
                "competition": nom_competition,
                "club": nom_club,
                "places": "7"},
            follow_redirects=True,
        )
        competition = next(
            competition
            for competition in competitions_data["competitions"]
            if competition["name"] == nom_competition
        )
        assert response_purchase_places.status_code == 200
        msg = b"Not enough places available in this competition"
        assert msg in response_purchase_places.data

    response_logout = client.get("/logout", follow_redirects=True)

    assert response_logout.status_code == 200
    assert b"Welcome" in response_logout.data
