from unittest.mock import patch


# test intégrations
def test_email_not_valid(client):
    response = client.post('/showSummary', data={
        'email': 'clubconnnu@example.com'},
        follow_redirects=True)
    assert response.status_code == 200
    assert b"Email inconnu" in response.data


def test_email_valid(client):
    response = client.post('/showSummary', data={
        'email': 'admin@irontemple.com'},
        follow_redirects=True)
    assert response.status_code == 200
    assert b"Email inconnu" not in response.data


def test_purchase_club_has_enough_points(
        client,
        mock_file_write,
        patch_clubs_and_competitions,
        clubs_data,
        competitions_data):

    nom_competition = competitions_data["competitions"][0]["name"]
    nom_club = clubs_data["clubs"][0]["name"]
    response = client.post('/purchasePlaces', data={
        'competition': nom_competition,
        'club': nom_club,
        'places': '2'
        },
        follow_redirects=True)

    # reconstruction data of dump to look inside de file mocked
    handle = mock_file_write()
    written = "".join(call.args[0] for call in handle.write.call_args_list)

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert mock_file_write().write.called
    assert nom_competition in written
    assert nom_club in written
    assert "48" in written


def test_purchase_club_has_not_enough_points(
        client,
        patch_clubs_and_competitions,
        clubs_data,
        competitions_data):

    club_points = clubs_data["clubs"][0]["points"]
    nom_competition = competitions_data["competitions"][0]["name"]
    nom_club = clubs_data["clubs"][0]["name"]
    response = client.post('/purchasePlaces', data={
        'competition': nom_competition,
        'club': nom_club,
        'places': '99'
        },
        follow_redirects=True)

    assert response.status_code == 200
    assert b"Insufficient points to complete this reservation" in response.data
    assert clubs_data["clubs"][0]["points"] == club_points


def test_purchase_more_than_12_places_should_fail(
        client,
        patch_clubs_and_competitions,
        clubs_data,
        competitions_data):

    nom_competition = competitions_data["competitions"][0]["name"]
    nom_club = clubs_data["clubs"][0]["name"]
    response = client.post('/purchasePlaces', data={
        'competition': nom_competition,
        'club': nom_club,
        'places': '13'
        },
        follow_redirects=True)

    assert response.status_code == 200
    assert b"One club cannot book more than 12 places for a single competition" in response.data
    assert competitions_data["competitions"][0]["numberOfPlaces"] == "25"


def test_purchase_12_or_less_places_should_succeed(
        client,
        mock_file_write,
        patch_clubs_and_competitions,
        clubs_data,
        competitions_data):

    nom_competition = competitions_data["competitions"][0]["name"]
    nom_club = clubs_data["clubs"][0]["name"]
    response = client.post('/purchasePlaces', data={
        'competition': nom_competition,
        'club': nom_club,
        'places': '2'
        },
        follow_redirects=True)

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert mock_file_write().write.called
    assert competitions_data["competitions"][0]["numberOfPlaces"] == "23"


def test_book_competition_when_future_date(
        client,
        patch_clubs_and_competitions):

    response = client.get('/book/Competition1/Club2')

    assert response.status_code == 200
    assert b"Places available" in response.data


def test_book_competition_when_passed_date(
        client,
        patch_clubs_and_competitions):

    response = client.get('/book/Competition2/Club2')

    assert response.status_code == 200
    assert b"must be superior or equal" in response.data


def test_show_clubs_displays_club_list_successfully(
        client,
        clubs_data):

    with patch("server.load_clubs", return_value=clubs_data["clubs"]):

        response = client.get('/showclubs')
        assert response.status_code == 200
        assert b"Club Points Table" in response.data
        assert b"Club1" in response.data
