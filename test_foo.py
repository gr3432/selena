import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager


timeout = 10

@pytest.fixture(scope="module")
def chrome_driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def edge_driver():
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    yield driver
    driver.quit()

@pytest.fixture(scope="module", params=("chrome_driver", "edge_driver"))
def driver(request):
    return request.getfixturevalue(request.param)


def test_foo(driver):
    driver.get("https://twitter.com")
    settings_locator = "//header//*//a[@aria-label='Settings']"
    condition = lambda driver: driver.find_element(By.XPATH, settings_locator)
    settings_link = WebDriverWait(driver, timeout=timeout).until(condition)
    settings_link.click()
    cookies_pref_locator = "//a[@href='/settings/cookie_preferences']"
    condition = lambda driver: driver.find_element(By.XPATH, cookies_pref_locator)
    cookies_pref = WebDriverWait(driver, timeout=timeout).until(condition)
    assert "Cookie" in cookies_pref.text

