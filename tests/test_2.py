from src.base_test import UiTestCase
from src.pages.login_page import LoginPage
from src.pages.main_page import MainPage
import allure
import  random

def login_as_standard_user(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

cart_address = "https://www.saucedemo.com/cart.html"
login_address = "https://www.saucedemo.com/"

@allure.epic("Website")
@allure.feature("Inventory")
class TestMain(UiTestCase):
    @allure.story("Login and get to the main page")
    def test_open_main_page(self):
        login_as_standard_user(self.driver)
        main_page = MainPage(self.driver)
        assert main_page.is_loaded()
        assert len(main_page.get_item_names()) > 0

    @allure.story("Adding an item to cart")
    def test_add_item(self):
        login_as_standard_user(self.driver)
        main_page = MainPage(self.driver)
        main_page.wait_until_loaded()
        items = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        main_page.add_item_to_cart(random.choice(items))
        self.assertEqual(
            1, main_page.get_cart_count(), f"There should be 1 item, "
                                        f"but actually there are {main_page.get_cart_count()}"
        )

    @allure.story("Adding several items to cart")
    def test_add_several_items(self):
        login_as_standard_user(self.driver)
        main_page = MainPage(self.driver)
        main_page.wait_until_loaded()
        items = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        main_page.add_item_to_cart(items[0])
        main_page.add_item_to_cart(items[1])
        main_page.add_item_to_cart(items[2])
        self.assertEqual(
            3, main_page.get_cart_count(), f"There should be 3 items, "
                                        f"but actually there are {main_page.get_cart_count()}"
        )

    @allure.story("Getting to the cart page")
    def test_get_cart_page(self):
        login_as_standard_user(self.driver)
        main_page = MainPage(self.driver)
        main_page.wait_until_loaded()
        main_page.open_cart()
        self.assertEqual(self.driver.current_url, cart_address)

    @allure.story("Logging out")
    def test_logout(self):
        login_as_standard_user(self.driver)
        main_page = MainPage(self.driver)
        main_page.wait_until_loaded()
        main_page.logout()
        self.assertEqual(self.driver.current_url, login_address)