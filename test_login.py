import pytest
from constants import test_email, test_password, login_page_url
from login_page import Login
from base_page import Basepage


@pytest.fixture(scope="function")
def login_page(driver):
    driver.get(login_page_url)
    login_page = Login(driver)
    yield login_page


def test_successful_login(login_page):
    login_page.select_ID_login()
    login_page.input_email(test_email)
    login_page.input_password(test_password)
    login_page.click_sign_in()
    login_page.select_stay_signed_in()
    base_page = Basepage(login_page.driver)
    assert base_page.page_loaded()
