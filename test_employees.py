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
    employees_page.search("")

def test_search_existing(page):
    page.search(existing_name)
    assert page.find_name_in_table(existing_name)

def test_search_not_existing(page):
    page.search(non_existing_name)
    assert not page.find_name_in_table(non_existing_name)

def test_search_empty(page):
    page.search("")
    assert page.find_name_in_table(existing_name)
