from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


TIMEOUT = 5


class Locators:
    ID_login_button = (By.XPATH, "//app-login-component/div/div/div[2]/div[1]/button")
    email_input = (By.NAME, "loginfmt")
    password_input = (By.XPATH, "//form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/input")
    sign_in_button = (By.ID, "idSIButton9")
    stay_signed_in_button = (By.XPATH, "//form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input")


class Login:
    def __init__(self, driver):
        self.driver = driver

    def select_ID_login(self):
        ID_login_button = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(Locators.ID_login_button))
        ID_login_button.click()

    def input_email(self, email):
        email_input = WebDriverWait(self.driver, TIMEOUT).until(
            lambda driver: driver.find_element(*Locators.email_input))
        email_input.send_keys(email)
        email_input.send_keys(Keys.ENTER)

    def input_password(self, password):
        password_input = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(Locators.password_input))
        password_input.send_keys(password)

    def click_sign_in(self):
        sign_in_button = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(Locators.sign_in_button))
        sign_in_button.click()

    def select_stay_signed_in(self):
        stay_signed_in_button = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(Locators.stay_signed_in_button))
        stay_signed_in_button.click()
    

