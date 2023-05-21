from employess_page import Employees
import pytest
from left_navigation_bar import LeftNavigationBar


existing_name = "Adam"
non_existing_name = "Bob"


@pytest.fixture(scope="module")
def get_employees_page(driver):
    left_navigation_bar = LeftNavigationBar(driver)
    left_navigation_bar.navigate_to_employees()
    yield
    left_navigation_bar.navigate_to_dashboard()
    assert driver.current_url.split('/')[-1] == "dashboard"

@pytest.fixture(scope="function")
def page(driver, get_employees_page):
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
