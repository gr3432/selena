from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


TIMEOUT = 10


class Locator():
    edit_profile_button = (By.XPATH, "//app-profile-details-info-card//app-details-info-card//div//div//button")
    first_name_input = (By.XPATH, "//app-profile-details-info-card/app-details-info-card/div/div[2]/div/app-profile-details-form/div[1]/app-text-input[1]/mat-form-field/div/div[1]/div[3]/input")
    first_name_text = (By.XPATH, "//app-profile-details-info-card/app-details-info-card/div/div[2]/div/app-profile-details-form/div[1]/app-text-input[1]/div[2]")
    save_profile_button = (By.XPATH, "//div//button[span[text()='Save']]")
    profile_details_header = (By.XPATH, "//app-profile-details/app-details-info-title/h3")


class Profile:
    def __init__(self, driver):
        self.driver = driver

    def get_profile_details_header(self):
        profile_details_header = WebDriverWait(self.driver, TIMEOUT).until(
            lambda driver: driver.find_element(*Locator.profile_details_header))
        return profile_details_header.text

    def edit_profile(self):
        edit_profile_button = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(Locator.edit_profile_button))
        actions = ActionChains(self.driver)
        actions.move_to_element(edit_profile_button).click().perform()
        ActionBuilder(self.driver).clear_actions()

    def get_first_name_text(self):
        first_name_text = WebDriverWait(self.driver, TIMEOUT).until(
            lambda driver: driver.find_element(*Locator.first_name_text))
        return first_name_text.text

    def edit_first_name(self, name):
        try:
            input_field = WebDriverWait(self.driver, TIMEOUT).until(
                lambda driver: driver.find_element(*Locator.first_name_input))
            input_field.clear()
            input_field.send_keys(name) 
        except TimeoutException:
            parent_loc = (By.XPATH, "//app-profile-details-info-card/app-details-info-card/div/div[2]/div/app-profile-details-form/div[1]/app-text-input[1]")
            parent = WebDriverWait(self.driver, TIMEOUT).until(
                lambda driver: driver.find_element(*parent_loc))
            print(parent.get_attribute("innerHTML"))
            raise TimeoutException
    
    def save_profile(self):
        # clickable means also enabled
        try:
            save_profile_button = WebDriverWait(self.driver, TIMEOUT).until(
                EC.element_to_be_clickable(Locator.save_profile_button))
            save_profile_button.click()
            return True
        except TimeoutException:
            return False
    

