import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager


@pytest.fixture(scope="session")
def driver():  
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument("--headless")

    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    return driver