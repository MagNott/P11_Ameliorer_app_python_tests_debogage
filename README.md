# gudlift-registration

## 1. Presentation
This is digital platform to coordinate strength competitions and their participants.
This project is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.


## 2. Getting Started

This project uses the following technologies:
* Python v3.x+
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    > Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. This keeps the project light-weight and easy to understand.
* [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)
    > This ensures you'll be able to install the correct packages without interfering with Python on your machine.

    >Before you begin, please ensure you have this installed globally. 


## 3. Setup & Installation

This project requires Python 3.10+ and uses a virtual environment.

To install and run the application locally:

1. Clone this repository:
   ``` bash
   git clone https://github.com/your-username/Python_Testing.git
   ```

2. Create and activate a virtual environment:
    ``` bash
    virtualenv .
    source bin/activate
    ```

3. Install all dependencies:
    ``` bash
    pip install -r requirements.txt
    ```

4. Set the environment variable (required for Flask to find the entry point):
    ``` bash
    export FLASK_APP=server.py
    ```

5. Run the application:
    ``` bash
    flask run
    ```

You should see the app running on http://127.0.0.1:5000/

## 4. Current Setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one.

The main ones are:

* competitions.json - list of competitions
* clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

The project structure is as follows:

``` bash
├── .coveragerc  # Coverage configuration file
├── CACHEDIR.TAG
├── README.md
├── clubs.json  # Club list
├── competitions.json  # Competition list
├── docs  # Screenshots and reports folder
│   ├── Flake8 report.png
│   ├── Performance charts.png
│   ├── Performance testing.png
│   └── Test coverage.png
├── locustfile.py  # Locust performance testing script
├── requirements.txt
├── server.py  # Main application file
├── setup.cfg  # Flake8 and black configuration file
├── templates  # HTML templates folder
│   ├── booking.html
│   ├── clubs.html
│   ├── index.html
│   └── welcome.html
├── tests  # Tests folder
│   ├── __init__.py
│   ├── conftest.py  # Pytest configuration file
│   ├── data  # Test data folder to locust
│   │   ├── clubs_test.json
│   │   └── competitions_test.json
│   ├── functional  # Functional tests folder
│   │   ├── __init__.py
│   │   └── test_functional.py
│   ├── integration  # Integration tests folder
│   │   ├── __init__.py
│   │   └── test_server.py
│   └── unit  # Unit tests folder
│       ├── __init__.py
│       └── test_utils.py
└── utils.py  # Utility functions
```

## 5. Testing

To do test driven development (TDD), we use:
* [pytest](https://docs.pytest.org/en/6.2.x/) - to run the tests
* [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) - to mock data and functions

To run the tests, we use pytest fixtures to set http client and mock data. This ensures that each test runs in isolation and does not affect other tests.

To launch the tests :
``` bash
pytest tests/
```

The coverage report is generated using the `--cov` option. To generate a coverage report, run:
``` bash
pytest --cov-config=.coveragerc --cov=. --cov-report=html tests/
``` 
The coverage report will be generated in the `htmlcov` folder. Open the `index.html` file in a web browser to view the report.

### Tests Coverage
![Tests coverage](docs/Test%20coverage.png)



## 6. Performance Testing - Locust

To do performance testing, we use:
* [Locust](https://locust.io/) - to simulate user traffic and measure performance

To launch locust, run:
``` bash
export FLASK_ENV=performance 
locust
```
Then open a web browser and go to `http://127.0.0.1:8089`

* You need to specify the number of users to simulate and the spawn rate. For example, to simulate 6 users enter `6` in the "Number of users to simulate" field.
* You need to specify the Host URL of the application running.
* Then click the "Start" button.

### This is the result of performance testing with 6 users.

![Performance testing](docs/Performance%20testing.png)

### This is the chart of the result of performance testing.

![Performance charts](docs/Performance%20charts.png)

## 7. Quality 

### Flake8 and Black
To ensure code quality and style, we use:
* [Black](https://black.readthedocs.io/en/stable/) - to format the code
``` bash
black .
``` 
* [Flake8](https://flake8.pycqa.org/en/latest/) - to ensure code style and quality 
``` bash
flake8 .
```
### Flake8 report

![Flake8 report](docs/Flake8%20report.png)

### Hungarian notation

To improve code readability, we use Hungarian notation for variable names in order to manipulate json data more easily.

* p = functions parameter
* d = dictionnary
* l = list
* l_dict = list of dictionaries

### Branch Naming Convention

>  Note: The default branch for this project is named `master`, following the original repository structure.

We use the following branch naming convention:
* `feature/branch-name` - for new features
* `bug/branch-name` - for bug fixes
* `quality/branch-name` - for code quality improvements
* `QA` - for review before integration


## 8. Corrections and improvements made
* Functional fixes :
    - Fix app crash when entering an unknown email
    - Prevent clubs from using more points than allowed
    - Disallow booking places in past competitions
    - Limit booking to 12 places per competition per club
    - Ensure point updates are correctly reflected
* New feature :
    - Implement Points Display Board accessible from the home and clubs pages
* Quality and testings improvements :
    - Improve code quality and style using Flake8 and Black
    - Add performance testing with Locust to simulate user traffic
    - Refactor utility functions for better readability and maintainability
    - Add unit, integration, and functional tests to ensure reliability
    - Enhance error handling for file operations to prevent crashes


## 9. External links

### Official Documentation
- https://flask.palletsprojects.com/en/stable/patterns/flashing/
- https://flask.palletsprojects.com/en/stable/quickstart/#debug-mode
- https://flask-fr.readthedocs.io/testing/#the-first-test
- https://docs.python.org/3/library/unittest.mock.html
- https://docs.pytest.org/en/6.2.x/fixture.html#teardown-cleanup-aka-fixture-finalization
- https://docs.python.org/3/library/datetime.html
- https://docs.python.org/fr/3.13/library/copy.html
- https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.call_args_list
- https://docs.locust.io/en/stable/installation.html
- https://docs.locust.io/en/stable/quickstart.html
- https://docs.python.org/3/library/exceptions.html#FileNotFoundError
- https://www.docstring.fr/formations/faq/resolution-derreurs/que-signifie-une-erreur-de-type-filenotfounderror/
- https://careerkarma.com/blog/python-jsondecodeerror/
- https://pytest-cov.readthedocs.io/en/latest/config.html


### Debugging discussion topics
- https://stackoverflow.com/questions/65694813/import-flask-could-not-be-resolved-from-source-pylance
- https://www.reddit.com/r/learnpython/comments/1070tb0/can_i_do_list_comprehension_with_a_multi_line/
- https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
- https://stackoverflow.com/questions/70743462/json-dumps-while-reading-file-as-mock-open


## 10. Author
This project was developed by Magnott in September 2025 as part of the Python Application Developer program at OpenClassrooms.


