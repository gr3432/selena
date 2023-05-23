from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class Locator:
    dashboard_button = (By.XPATH, "//app-left-nav/aside/ul/li[1]/a")
    organization_button = (By.XPATH, "//app-left-nav/aside/ul/li[2]/a")
    organization_submenu = (By.XPATH, "//app-left-nav/aside/ul/li[2]/ul")
    employees_button = (By.XPATH, "//app-left-nav/aside/ul/li[2]/ul/li[2]/a")


class LeftNavigationBar:
    """
    Representation of the Left Navigation Bar
    """
    def __init__(self, driver):
        self.driver = driver

    def navigate_to_dashboard(self):
        dashboard_button = self.driver.find_element(*Locator.dashboard_button)
        dashboard_button.click()

    def navigate_to_employees(self):
        organization_button = self.driver.find_element(*Locator.organization_button)
        if not "open" in organization_button.find_element(By.XPATH, "./div[2]").get_attribute("class"):
            ActionChains(self.driver).move_to_element(organization_button).click().perform()
        organization_submenu = self.driver.find_element(*Locator.organization_submenu)
        if "opacity: 0" in organization_submenu.get_attribute("style"):
            ActionChains(self.driver).move_to_element(organization_button).click().perform()
        employees_button = self.driver.find_element(*Locator.employees_button)
        employees_button.click()
