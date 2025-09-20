from flask import Flask, render_template, request, redirect, flash, url_for
from utils import get_club_by_email, get_club_by_name, get_competition_by_name
from utils import update_clubs_in_json, update_competitions_in_json
from utils import load_clubs, load_competitions
from datetime import datetime


app = Flask(__name__)
app.secret_key = "something_special"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
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
    l_dict_competitions = load_competitions()
    l_dict_clubs = load_clubs()
    today_date = datetime.now()

    email_connexion = request.form["email"]
    try:
        selected_club = get_club_by_email(l_dict_clubs, email_connexion)
    except IndexError:
        flash("Email inconnu")
        return redirect("/")

    return render_template(
        "welcome.html",
        club=selected_club,
        competitions=l_dict_competitions,
        today_date=today_date,
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Display the booking page for a club and competition.

    If the competition is in the past, show an error and return to the home
    page.
    Otherwise, render the booking page.

    Args:
        competition (str): Name of the competition.
        club (str): Name of the club.

    Returns:
        Rendered HTML page (booking or welcome).
    """
    l_dict_competitions = load_competitions()
    l_dict_clubs = load_clubs()

    try:
        name_club = club
        selected_club = get_club_by_name(l_dict_clubs, name_club)

        name_competition = competition
        selected_competition = get_competition_by_name(
            l_dict_competitions, name_competition
        )

    except IndexError:
        flash("Club or Competition cannot be found, please log in again !")
        return redirect("/")

    today_date = datetime.now()

    date_competition = selected_competition["date"]
    if date_competition < today_date:
        flash("Competition's date must be superior or equal to today's date")
        return render_template(
            "welcome.html",
            club=selected_club,
            competitions=l_dict_competitions,
            today_date=today_date,
        )
    elif selected_club and selected_competition:
        return render_template(
            "booking.html",
            club=selected_club,
            competition=selected_competition,
            today_date=today_date,
        )


@app.route("/purchasePlaces", methods=["POST"])
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
    l_dict_competitions = load_competitions()
    l_dict_clubs = load_clubs()
    today_date = datetime.now()

    try:
        name_competition = request.form["competition"]
        selected_competition = get_competition_by_name(
            l_dict_competitions, name_competition
        )

        name_club = request.form["club"]
        selected_club = get_club_by_name(l_dict_clubs, name_club)

    except IndexError:
        flash("The club or the competition cannot be found")
        return redirect("/")

    points_club = int(selected_club["points"])
    places_required = int(request.form["places"])

    if places_required > points_club:
        flash("Insufficient points to complete this reservation")
    elif places_required > 12:
        flash("One club cannot book more than 12 places for a competition")
    elif places_required > int(selected_competition["numberOfPlaces"]):
        flash("Not enough places available in this competition")
    else:
        points_competition = int(selected_competition["numberOfPlaces"])

        selected_competition["numberOfPlaces"] = str(
            points_competition - places_required
        )
        update_competitions_in_json(l_dict_competitions)

        flash("Great-booking complete!")

        selected_club["points"] = str(points_club - places_required)
        update_clubs_in_json(l_dict_clubs)

    return render_template(
        "welcome.html",
        club=selected_club,
        competitions=l_dict_competitions,
        today_date=today_date,
    )


@app.route("/showclubs")
def list_clubs():
    l_dict_clubs = load_clubs()
    return render_template("clubs.html", clubs=l_dict_clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
