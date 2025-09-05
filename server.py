import json
from flask import Flask, render_template, request, redirect, flash, url_for
from utils import get_club_by_email, get_club_by_name, get_competition_by_name, update_clubs_in_json, update_competitions_in_json


app = Flask(__name__)
app.secret_key = 'something_special'


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
    return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
    return listOfCompetitions


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """
    Authenticate a club using its email and display a personalized homepage.

    This view is triggered after submitting the login form.
    It retrieves the submitted email, looks up the corresponding club using the
    `email_validation()` function, and then renders the 'welcome.html'
    template with club and competition information.

    If the email is not recognized, the user is redirected to the homepage
    with a flash message.

    Returns:
        - Renders 'welcome.html' with the selected club and a list of
          competitions.
        - Redirects to '/' if the email is invalid.
    """
    l_dict_competitions = loadCompetitions()
    l_dict_clubs = loadClubs()

    email_connexion = request.form['email']
    try:
        selected_club = get_club_by_email(l_dict_clubs, email_connexion)
    except IndexError:
        flash("Email inconnu")
        return redirect("/")

    return render_template(
        'welcome.html',
        club=selected_club,
        competitions=l_dict_competitions
    )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    l_dict_competitions = loadCompetitions()
    l_dict_clubs = loadClubs()

    name_club = club
    selected_club = get_club_by_name(l_dict_clubs, name_club)

    name_competition = competition
    selected_competition = get_competition_by_name(
        l_dict_competitions,
        name_competition)

    if selected_club and selected_competition:
        return render_template(
            'booking.html',
            club=selected_club,
            competition=selected_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html',
            club=selected_club,
            competitions=selected_competition
        )


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    """
    Manage to book places of competition. This route processes a POST
    request to reserve a number of places for a club in a specific competition.
    - Retrieves club and competition from form data.
    - Checks if the club has enough points.
    - Checks if the club try to book more than 12 places on a competition
    - If valid, deducts points and updates available places.
    - Saves updated competition data to JSON
    - Saves updated club data to JSON.
    - Displays success or error message.

    Returns:
        Rendered 'welcome.html' with updated data.
    """
    l_dict_competitions = loadCompetitions()
    l_dict_clubs = loadClubs()

    try:
        name_competition = request.form['competition']
        selected_competition = get_competition_by_name(
            l_dict_competitions,
            name_competition
        )

        name_club = request.form['club']
        selected_club = get_club_by_name(
            l_dict_clubs,
            name_club
        )

    except IndexError:
        flash("The club or the competition cannot be found")
        return redirect("/")

    points_club = int(selected_club["points"])
    places_required = int(request.form['places'])

    if places_required > points_club:
        flash('Insufficient points to complete this reservation')
    elif places_required > 12:
        flash('One club cannot book more than 12 places for a single competition')
    else:
        points_competition = int(selected_competition['numberOfPlaces'])

        selected_competition['numberOfPlaces'] = str(points_competition - places_required)
        update_competitions_in_json(l_dict_competitions)

        flash('Great-booking complete!')

        selected_club['points'] = str(points_club - places_required)
        update_clubs_in_json(l_dict_clubs)

    return render_template(
        'welcome.html',
        club=selected_club,
        competitions=l_dict_competitions
    )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
