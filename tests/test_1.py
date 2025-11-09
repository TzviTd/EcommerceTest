import unittest
from src.base_test import UiTestCase
from src.pages.login_page import LoginPage
import allure

@allure.epic("Website")
@allure.feature("Auth")
class TestLogin(UiTestCase):
    @allure.story("Valid Login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self):
         page = LoginPage(self.driver)
         page.open()
         page.login("standard_user", "secret_sauce")
         page.wait_success()
    @allure.story("Invalid Password")
    def test_invalid_password(self):
        page = LoginPage(self.driver)
        page.open()
        page.login("standard_user", "wrongpAssword")
        msg = page.wait_error()
        self.assertIsNotNone(msg)
        self.assertIn("Username and password do not match", msg)

    @allure.story("Invalid Username")
    def test_invalid_username(self):
        page = LoginPage(self.driver)
        page.open()
        page.login("another_user", "secret_sauce")
        msg = page.wait_error()
        self.assertIsNotNone(msg)
        self.assertIn("Username and password do not match", msg)

    @allure.story("Invalid both Username and Password")
    def test_invalid_username_and_password(self):
        page = LoginPage(self.driver)
        page.open()
        page.login("another_user", "we")
        msg = page.wait_error()
        self.assertIsNotNone(msg)
        self.assertIn("Username and password do not match", msg)

    @allure.story("Invalid: Login with empty fields")
    def test_empty_fields(self):
        page = LoginPage(self.driver)
        page.open()
        page.login("", "")
        msg = page.wait_error()
        self.assertIsNotNone(msg)
        self.assertIn("Username is required", msg)

    @allure.story("Invalid: Login as locked out user")
    def test_locked_out_user(self):
        page = LoginPage(self.driver)
        page.open()
        page.login("locked_out_user", "secret_sauce")
        msg = page.wait_error()
        self.assertIsNotNone(msg)
        self.assertIn("Sorry, this user has been locked out", msg)


if __name__ == "__main__":
     unittest.main()
