import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from constants import webdriver_edge_path


@pytest.fixture(scope="session")
def driver():  
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    service = Service(executable_path=webdriver_edge_path)
    driver = webdriver.Edge(service=service, options=options)
    
    return driver