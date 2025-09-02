# gudlift-registration

## 1. Why
This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.


## 2. Getting Started

This project uses the following technologies:

* Python v3.x+

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)

    Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
    

* [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

    This ensures you'll be able to install the correct packages without interfering with Python on your machine.

    Before you begin, please ensure you have this installed globally. 


## 3. Setup & Installation

This project requires Python 3.10+ and uses a virtual environment.

To install and run the application locally:

1. Clone this repository:
   ```
   git clone https://github.com/your-username/Python_Testing.git
   ```

2. Create and activate a virtual environment:
    ```
    virtualenv .
    source bin/activate
    ```

3. Install all dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Set the environment variable (required for Flask to find the entry point):
    ```
    export FLASK_APP=server.py
    ```

5. Run the application:
    ```
    flask run
    ```

You should see the app running on http://127.0.0.1:5000/

## 4. Current Setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
    
* competitions.json - list of competitions
* clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

## 5. Testing

You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

We also like to show how well we're testing, so there's a module called 
[coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.


## 6. Liens externes

### Documentation officielle
- https://flask.palletsprojects.com/en/stable/patterns/flashing/
- https://flask.palletsprojects.com/en/stable/quickstart/#debug-mode
- https://flask-fr.readthedocs.io/testing/#the-first-test

### Sujets discussion à des fins de debug
- https://stackoverflow.com/questions/65694813/import-flask-could-not-be-resolved-from-source-pylance
- https://www.reddit.com/r/learnpython/comments/1070tb0/can_i_do_list_comprehension_with_a_multi_line/
- https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask


## 7. convention de nommage

Notation hongroise : 
d = dictionnaire
l_dict = liste de dictionnaire


>  Note: The default branch for this project is named `master`, following the original repository structure.


