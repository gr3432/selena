import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager


timeout = 10


@pytest.fixture(scope="module")
def chrome_driver():
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def edge_driver():
    options = EdgeOptions()
    options.add_argument("--headless")
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="module", params=("chrome_driver", "edge_driver"))
def driver(request):
    return request.getfixturevalue(request.param)


def test_foo(driver):
    driver.get("https://magento.softwaretestingboard.com/")
    promotions_locator = "//a[.//*//strong[text()='20% OFF']]"
    condition = lambda driver: driver.find_element(By.XPATH, promotions_locator)
    promotions_link = WebDriverWait(driver, timeout=timeout).until(condition)
    promotions_link.click()
    heading_locator = "//h1[@id='page-title-heading']//span"
    condition = lambda driver: driver.find_element(By.XPATH, heading_locator)
    heading = WebDriverWait(driver, timeout=timeout).until(condition)
    assert "Pants" in heading.text

