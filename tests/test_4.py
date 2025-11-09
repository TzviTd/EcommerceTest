from src.base_test import UiTestCase
from src.pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage
from src.pages.main_page import MainPage
from tests.test_3 import get_cart_page, ITEMS
import math
import allure


@allure.epic("Website")
@allure.feature("Checkout")
class TestCheckoutPage(UiTestCase):
    @allure.story("Open checkout page")
    def test_open_checkout_page(self):
        cart = get_cart_page(self.driver, items=ITEMS)
        cart.proceed_to_checkout()
        step_1 = CheckoutStepOnePage(self.driver)
        step_1.wait_until_loaded()

        with allure.step(f"Current URL: {self.driver.current_url}"):
            pass

        self.assertTrue(step_1.is_loaded())
        self.assertTrue(step_1.is_loaded(), f"Not on step-one, url={self.driver.current_url}")

    @allure.story("Finish the order successfully")
    def test_successful_checkout(self):
        cart = get_cart_page(self.driver, items=ITEMS)
        prices = cart.get_item_prices()
        expected_subtotal = round(sum(prices), 2)

        cart.proceed_to_checkout()
        with allure.step(f"URL: {self.driver.current_url}"): pass

        step_1 = CheckoutStepOnePage(self.driver)
        step_1.wait_until_loaded()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        self.assertTrue(step_1.is_loaded(), f"Not on step-one | {self.driver.current_url}")

        step_1.fill_in_the_form("John", "Doe", "12345")
        step_1.proceed_to_payment()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        step_2 = CheckoutStepTwoPage(self.driver)
        step_2.wait_until_loaded()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        self.assertTrue(step_2.is_loaded(), f"Not on step-two | {self.driver.current_url}")

        items_overview = step_2.get_item_names()
        self.assertCountEqual(items_overview, ITEMS)

        subtotal = step_2.get_subtotal()
        self.assertTrue(
            math.isclose(subtotal, expected_subtotal, abs_tol=0.01),
            f"Subtotal mismatch: overview={subtotal} vs cart_sum={expected_subtotal}"
        )

        step_2.finish()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        step_3 = CheckoutCompletePage(self.driver)
        self.assertTrue(step_3.is_loaded(), f"Not on complete | {self.driver.current_url}")
        self.assertIn("Thank you for your order!", step_3.get_header_text())

    @allure.story("Invalid test: let the fields empty")
    def test_empty_fields(self):
        cart = get_cart_page(self.driver, items=ITEMS)
        cart.proceed_to_checkout()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        step_1 = CheckoutStepOnePage(self.driver)
        step_1.wait_until_loaded()
        self.assertTrue(step_1.is_loaded())

        step_1.fill_in_the_form("", "", "")
        step_1.proceed_to_payment(require_values=False)
        err = step_1.wait_for_error(timeout=10)  # ← ключевая строка
        self.assertIsNotNone(err, f"No error visible | url={self.driver.current_url}")
        self.assertIn("First Name is required", err)

    @allure.story("Cancel the purchase")
    def test_cancel(self):
        cart = get_cart_page(self.driver, items=ITEMS)
        cart.proceed_to_checkout()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        step_1 = CheckoutStepOnePage(self.driver)
        step_1.wait_until_loaded()
        self.assertTrue(step_1.is_loaded())

        step_1.fill_in_the_form("John", "Doe", "12345")
        step_1.proceed_to_payment()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        step_2 = CheckoutStepTwoPage(self.driver)
        step_2.wait_until_loaded()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        self.assertTrue(step_2.is_loaded())

        step_2.cancel()

        with allure.step(f"URL: {self.driver.current_url}"): pass

        main = MainPage(self.driver)
        main.wait_until_loaded()
        self.assertIn("inventory", self.driver.current_url)