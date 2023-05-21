from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


TIMEOUT = 5


class Locators:
    employees_list_header = (By.XPATH, "//app-employees-list/app-view-base-layout/div/app-view-header/div/app-page-header/div/div/div[1]/h2")
    search_input = (By.XPATH, "//input[@placeholder='Enter keyword to search...']")
    result_table_names = "//mat-table[@role='table']//mat-row//mat-cell[2]//span"
    table = (By.XPATH, "//app-universal-table/div/div/mat-table")



class Employees:
    def __init__(self, driver):
        self.driver = driver

    def get_employees_list_header(self):
        employees_list_header = WebDriverWait(self.driver, TIMEOUT).until(
            lambda driver: driver.find_element(*Locators.employees_list_header))
        return employees_list_header.text

    def search(self, query):
        search_input = WebDriverWait(self.driver, TIMEOUT).until(
            lambda driver: driver.find_element(*Locators.search_input))
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN) # needed?

    def find_name_in_table(self, name):
        table_xpath = Locators.table[1]
        row_based_on_name_locator = (By.XPATH, f"{table_xpath}/mat-row[./mat-cell[2]/span[text()='{name}']]")
        try:
            rows = WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_all_elements_located(row_based_on_name_locator))
            return rows
        except TimeoutException:
            return []
        
    def navigate_to_name(self, name):
        names = self.find_name_in_table(name)
        assert len(names) == 1
        names[0].click()
