

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
