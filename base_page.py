from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

TIMEOUT = 10

class Locators:
    top_bar_header = (By.XPATH, "//app-top-bar/mat-toolbar/div[1]/span")

class Basepage:
    """
    Representation of the basic elements of the app
    """
    def __init__(self, driver):
        self.driver = driver

    def page_loaded(self):
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                lambda driver: driver.find_element(*Locators.top_bar_header)
            )
            return True
        except TimeoutException:
            return False
    