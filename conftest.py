import pytest
import pickle
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from constants import login_page_url, landing_page_url


@pytest.fixture(scope="session")
def driver():  
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument("--headless")

    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    return driver

@pytest.fixture(scope="session")
def driver_with_cookies():
    # cookies.pkl was created with pickle.dump
    with open("cookies.pkl", "rb") as f:
        cookies = pickle.load(f)

    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service)

    driver.get(login_page_url)
    
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    driver.get(landing_page_url)
    
    yield driver

    driver.quit()