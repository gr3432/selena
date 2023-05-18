from employess_page import Employees
import time
import pytest

# TODO replace time.sleep(search_wait) with wait-until-search-returns
search_wait = 2
existing_name = "Adam"
non_existing_name = "Bob"


@pytest.fixture
def page(driver):
    employees_page = Employees(driver)
    yield employees_page
    employees_page.search_input.clear()

def test_search_existing(page):
    page.search_input.clear()
    page.search(existing_name)
    time.sleep(search_wait)
    names = page.get_employee_names()
    assert existing_name in names

def test_search_not_existing(page):
    page.search_input.clear()
    page.search(non_existing_name)
    time.sleep(search_wait)
    names = page.get_employee_names()
    assert not(non_existing_name in names)

def test_search_empty(page):
    page.search_input.clear()
    page.search("")
    time.sleep(search_wait)
    names = page.get_employee_names()
    assert existing_name in names