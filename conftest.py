import pytest
import pickle
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from login_page import Login
from base_page import Basepage


########## Pytest configuration ##########
def pytest_addoption(parser):
    """
    Add extra options to pytest
    """
    parser.addoption(
        "--headless",
        action = "store_true",
        help = "Run driver in headless mode"
    )
    # Environment secrets are used by CI
    # If not specified it will look for sensitive data in constants.json
    # See also pytest_configure
    parser.addoption(
        "--environment-secrets",
        action = "store_true",
        help = "Look for secrets in environment instead of constants.json"
    )

def pytest_configure(config):
    if config.getoption("--environment-secrets"):
        import os
        pytest.test_email = os.environ['TEST_EMAIL']
        pytest.test_password = os.environ['TEST_PASSWORD']
        pytest.login_page_url = os.environ['LOGIN_PAGE_URL']
    else:
        from constants import test_email, test_password, login_page_url
        pytest.test_email = test_email
        pytest.test_password = test_password
        pytest.login_page_url = login_page_url


########## Setup and Tear down code for test run session ##########
@pytest.fixture(scope="session")
def edge_driver(request):
    options = EdgeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless")
    service = EdgeService(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=options)

@pytest.fixture(scope="session")
def chrome_driver(request):
    options = ChromeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

@pytest.fixture(scope="session", params=("chrome_driver", "edge_driver"))
def driver_with_login(request):
    driver = request.getfixturevalue(request.param)    

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
    """
    An alternative browser configuration can be selected here
    """
    return driver_with_login


########## Alternative configurations for drivers ##########
@pytest.fixture(scope="session")
def driver_already_opened():
    """
    Only used for test development.
    It will use an already opened browser and it will not close browser after
    test session is finished.
    """
    options = EdgeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    return driver

@pytest.fixture(scope="session")
def driver_with_cookies():
    """
    Loading presaved session cookies to avoid having to re-login.
    Currently not working.
    """
    # cookies.pkl was created with pickle.dump
    with open("cookies.pkl", "rb") as f:
        cookies = pickle.load(f)

    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)

    driver.get(pytest.login_page_url)
    
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    driver.get(pytest.landing_page_url)
    
    yield driver

    driver.quit()