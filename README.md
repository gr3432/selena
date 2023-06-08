# selena
Testing web application with Selenium using Page Object Model.

## Prerequisites
1. Install python from https://www.python.org/. Code has been tested with python version 3.8 and 3.10.
2. Create a virtual environment.
   > python -m venv venv
3. Activate virtual environment.
   > venv/Scripts/activate
4. Install dependencies.
   > pip install -r requirements.txt
5. Fill in user email, user password and login page url in constants.json.

## How to run
### Run all the tests
Just run pytest inside the virtual environment.
  > pytest

### Run a subset of tests
To run only tests from one module specify the name of the module after pytest. For example:
  > pytest test_employees.py

## Continuous Integration
See Actions tab on GitHub. Runs are triggered manually. Workflow description in .github/workflows/webdriver-test.yml.
