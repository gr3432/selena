import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


TIMEOUT = 5


class Locator():
    edit_profile_button = (By.XPATH, "//app-profile-details-info-card//app-details-info-card//div//div//button")
    first_name_input = (By.XPATH, "//app-profile-details-info-card/app-details-info-card/div/div[2]/div/app-profile-details-form/div[1]/app-text-input[1]/mat-form-field/div/div[1]/div[3]/input")
    first_name_text = (By.XPATH, "//app-profile-details-info-card/app-details-info-card/div/div[2]/div/app-profile-details-form/div[1]/app-text-input[1]/div[2]")
    save_profile_button = (By.XPATH, "//div//button[span[text()='Save']]")


class Profile:
    """
    Representation of the Employee profile details page
    """
    def __init__(self, driver):
        self.driver = driver
        self.edit_profile_button = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(Locator.edit_profile_button))

    def edit_profile(self):        
        actions = ActionChains(self.driver)
        actions.move_to_element(self.edit_profile_button).click().perform()
        time.sleep(5)

    def get_first_name_text(self):
        first_name_text = WebDriverWait(self.driver, TIMEOUT).until(
            lambda driver: driver.find_element(*Locator.first_name_text))
        return first_name_text.text

    def edit_first_name(self, name):
        input_field = WebDriverWait(self.driver, TIMEOUT).until(
            lambda driver: driver.find_element(*Locator.first_name_input))
        input_field.clear()
        input_field.send_keys(name)

    def save_profile(self):
        try:
            save_profile_button = WebDriverWait(self.driver, TIMEOUT).until(
                EC.element_to_be_clickable(Locator.save_profile_button))
            save_profile_button.click()
            return True
        except TimeoutException:
            return False
