from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Locators:
    search_input = "//input[@placeholder='Enter keyword to search...']"
    result_table_names = "//mat-table[@role='table']//mat-row//mat-cell[2]//span"


class Employees:
    def __init__(self, driver):
        self.driver = driver
        self.search_input = driver.find_element(By.XPATH, Locators.search_input)

    def search(self, query):
        self.search_input.send_keys(query)
        self.search_input.send_keys(Keys.RETURN)
    
    def get_employee_names(self):
        return [name.text for name in self.driver.find_elements(By.XPATH, Locators.result_table_names)]