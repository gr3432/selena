import pytest
from employess_page import Employees
from left_navigation_bar import LeftNavigationBar


@pytest.fixture(scope="module")
def get_employees_page(driver):
    """
    Workaround to navigate to employees list page
    since loading directly from url would require re-login.
    After tests in this module are finished, return to dashboard page.
    """
    left_navigation_bar = LeftNavigationBar(driver)
    left_navigation_bar.navigate_to_employees()
    yield
    left_navigation_bar.navigate_to_dashboard()
    assert driver.current_url.split('/')[-1] == "dashboard"

@pytest.fixture(scope="function")
def page(driver, get_employees_page):
    """
    Set up and Tear down code for every test

    Set up should load profile details page, but since cookies do not work
    use get_profile_page workaround.

    Tear down contains clean up code in case something went wrong with the test 
    to ensure that the state of the app is the same as when test started.
    """
    employees_page = Employees(driver)
    yield employees_page
    employees_page.search("")


########## Test Cases ##########
def test_search_unique_match(page):
    page.search("Adam")
    assert page.get_names_from_table() == ["Adam"]

def test_search_no_matches(page):
    page.search("Bob")
    assert not page.get_names_from_table()

def test_search_empty(page):
    page.search("")
    assert page.get_names_from_table()

def test_search_with_mulitple_matches(page):
    page.search("Automation")
    assert len(page.get_names_from_table()) > 1
