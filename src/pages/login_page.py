from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure

class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.username = (By.ID, "user-name")
        self.password = (By.ID, "password")
        self.login_btn = (By.ID, "login-button")
        self.error = (By.CSS_SELECTOR, "[data-test='error']")  # h3 "Epic sadface: ..."

    @allure.step("Open login page")
    def open(self):
        self.driver.get(self.URL)

    def _set_input(self, locator, text: str, timeout: int = 10):
        w = WebDriverWait(self.driver, timeout)
        el = w.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.DELETE)
        if text:
            el.send_keys(text)

    @allure.step("Fill credentials")
    def fill_credentials(self, username: str, password: str):
        self._set_input(self.username, username)
        self._set_input(self.password, password)

    @allure.step("Submit login form")
    def submit(self, timeout: int = 10):
        w = WebDriverWait(self.driver, timeout)
        btn = w.until(EC.presence_of_element_located(self.login_btn))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        try:
            w.until(EC.element_to_be_clickable(self.login_btn)).click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)


    @allure.step("Login (no implicit wait for result)")
    def login(self, username: str, password: str):
        """Login without waiting for inventory page"""
        self.fill_credentials(username, password)
        self.submit()

    @allure.step("Wait login success (inventory)")
    def wait_success(self, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.url_contains("inventory"))

    @allure.step("Wait login error")
    def wait_error(self, timeout: int = 10) -> str | None:
        w = WebDriverWait(self.driver, timeout)
        try:
            el = w.until(EC.visibility_of_element_located(self.error))
            return el.text.strip()
        except TimeoutException:
            return None

    def get_error_text(self) -> str | None:
        els = self.driver.find_elements(*self.error)
        return els[0].text.strip() if els and els[0].is_displayed() else None

