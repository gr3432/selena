import pytest
import pickle
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from login_page import Login
from base_page import Basepage


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action = "store_true",
        help = "Run driver in headless mode"
    )
    parser.addoption(
        "--environment-secrets",
        action = "store_true",
        help = "Look for secrets in environment"
    )

def pytest_configure(config):
    if config.getoption("--environment-secrets"):
        import os
        pytest.test_email = os.environ['test_email']
        pytest.test_password = os.environ['test_password']
        pytest.login_page_url = os.environ['login_page_url']
    else:
        from constants import test_email, test_password, login_page_url
        pytest.test_email = test_email
        pytest.test_password = test_password
        pytest.login_page_url = login_page_url


@pytest.fixture(scope="session")
def driver_already_opened():  
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument("--headless")

    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    return driver

@pytest.fixture(scope="session")
def driver_with_login(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless")
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)

    driver.maximize_window()
    driver.get(pytest.login_page_url)

    login_page = Login(driver)
    login_page.select_ID_login()
    login_page.input_email(pytest.test_email)
    login_page.input_password(pytest.test_password)
    login_page.click_sign_in()
    login_page.select_stay_signed_in()
    base_page = Basepage(login_page.driver)
    assert base_page.page_loaded()

    yield driver

    driver.quit()

@pytest.fixture(scope="session")
def driver(driver_with_login):
    return driver_with_login

@pytest.fixture(scope="session")
def driver_with_cookies():
    # cookies.pkl was created with pickle.dump
    with open("cookies.pkl", "rb") as f:
        cookies = pickle.load(f)

    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)

    driver.get(pytest.login_page_url)
    
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    driver.get(pytest.landing_page_url)
    
    yield driver

    driver.quit()