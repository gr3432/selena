import pytest
from left_navigation_bar import LeftNavigationBar
from employess_page import Employees
from profile_page import Profile


def reset_page(driver):
    """
    Workaround to refresh a page, since driver.refresh() would require re-login
    """
    driver.back()
    driver.forward()

@pytest.fixture(scope="module")
def get_profile_page(driver):
    """
    Workaround to navigate to profile details page
    since loading directly from url would require re-login.
    After tests in this module are finished, return to dashboard page.
    """
    # Set up
    left_navigation_bar = LeftNavigationBar(driver)
    left_navigation_bar.navigate_to_employees()
    employees_page = Employees(driver)
    employees_page.navigate_to_name("Adam")
    yield
    # Tear down
    left_navigation_bar.navigate_to_dashboard()
    assert driver.current_url.split('/')[-1] == "dashboard"

@pytest.fixture(scope="function")
def page(driver, get_profile_page):
    """
    Set up and Tear down code for every test

    Set up should load profile details page, but since cookies do not work
    use get_profile_page workaround.

    Tear down contains clean up code in case something went wrong with the test 
    to ensure that the state of the app is the same as when test started.
    Since we cannot reload page in the setup here we use the reset_page 
    workaround to ensure next page starts from fresh profile details page.
    """
    # Set up
    profile_page = Profile(driver)
    yield profile_page
    # Tear down
    reset_page(driver)


########## Test Cases ##########
@pytest.mark.parametrize("name", ["Björn", "Mary-Kate", "Adam"])
def test_edit_first_name(page, name):
    # last name in the list should always be the existing name 
    # so the test does not change data
    page.edit_profile()
    page.edit_first_name(name)
    assert page.save_profile()
    assert page.get_first_name_text() == name

@pytest.mark.skip(reason="Save button is enabled with empty obligatory field")
def test_leave_first_name_empty(page):
    page.edit_profile()
    page.edit_first_name("")
    assert not page.save_profile()
    reset_page(page.driver)
    assert page.get_first_name_text() == "Adam"

def test_interrupt_editing_first_name(page):
    page.edit_profile()
    page.edit_first_name("Nick")
    reset_page(page.driver)
    assert page.get_first_name_text() == "Adam"
    