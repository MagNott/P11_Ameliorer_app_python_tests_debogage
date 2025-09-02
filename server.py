import json
from flask import Flask, render_template, request, redirect, flash, url_for
from utils import get_club_by_email


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


l_dict_competitions = loadCompetitions()
l_dict_clubs = loadClubs()


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
def book(competition,club):
    foundClub = [c for c in l_dict_clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in l_dict_clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__": app.run(debug=True)