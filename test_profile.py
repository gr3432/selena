from profile_page import Profile
import pytest
from left_navigation_bar import LeftNavigationBar
from employess_page import Employees


def reset_profile_details_page(page):
    page.view_organization_unit()
    assert page.get_organization_unit_header() == "ORGANIZATION UNIT"
    page.view_profile_details()
    page.get_profile_details_header()
    assert page.get_profile_details_header() == "PROFILE DETAILS"

@pytest.fixture(scope="module")
def get_profile_page(driver):
    # Set up
    left_navigation_bar = LeftNavigationBar(driver)
    left_navigation_bar.navigate_to_employees()
    assert driver.current_url.split('/')[-1] == "employees"
    employees_page = Employees(driver)
    employees_page.navigate_to_name("Adam")
    yield
    # Tear down
    left_navigation_bar.navigate_to_dashboard()
    assert driver.current_url.split('/')[-1] == "dashboard"

@pytest.fixture(scope="function")
def page(driver, get_profile_page):
    # Set up
    profile_page = Profile(driver)
    # make sure current page is profile page
    assert profile_page.get_profile_details_header() == "PROFILE DETAILS"
    yield profile_page
    # Tear down
    # in case something went wrong with the test
    # replace with page refresh when cookies work
    reset_profile_details_page(profile_page)


# last name should always be the existing name so the test does not change data
@pytest.mark.parametrize("name", ["Björn", "Mary-Kate", "Adam"])
def test_edit_first_name(page, name):
    page.edit_profile()
    page.edit_first_name(name)
    assert page.save_profile()
    assert page.get_first_name_text() == name

@pytest.mark.skip(reason="Save button is enabled with empty obligatory field")
def test_leave_first_name_empty(page):
    page.edit_profile()
    page.edit_first_name("")
    assert not page.save_profile()
    reset_profile_details_page(page)
    assert page.get_first_name_text() == "Adam"

@pytest.mark.parametrize("name", ["A"])
def test_invalid_first_names(page, name):
    page.edit_profile()
    page.edit_first_name(name)
    assert page.save_profile()
    assert page.get_first_name_text() == "Adam"
    