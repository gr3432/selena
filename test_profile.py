from profile_page import Profile
import time
import pytest


# Helpers
def check_personnummer(number):
    digits = [int(c) for c in reversed(number) if c.isdigit()]
    if len(digits) != 10:
        return False
    even_digits = [d if d < 5 else d - 9 for d in digits[1::2]]
    return sum(digits + even_digits) % 10 == 0

def reset_profile_details_page(page):
    page.view_organization_unit()
    assert page.get_organization_unit_header() == "ORGANIZATION UNIT"
    page.view_profile_details()
    page.get_profile_details_header()
    assert page.get_profile_details_header() == "PROFILE DETAILS"


@pytest.fixture
def page(driver):
    # Set up
    profile_page = Profile(driver)
    # make sure current page is profile page
    reset_profile_details_page(profile_page)
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

def test_leave_first_name_empty(page):
    page.edit_profile()
    page.edit_first_name("")
    time.sleep(2)
    assert not page.save_profile()
    reset_profile_details_page(page)
    assert page.get_first_name_text() == "Adam"

@pytest.mark.parametrize("name", ["A"])
def test_invalid_first_names(page, name):
    page.edit_profile()
    page.edit_first_name(name)
    assert page.save_profile()
    assert page.get_first_name_text() == "Adam"
    