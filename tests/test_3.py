from src.base_test import UiTestCase
from src.pages.cart_page import CartPage
from src.pages.main_page import MainPage
from tests.test_2 import login_as_standard_user
import allure

ITEMS = ["Sauce Labs Backpack", "Sauce Labs Bike Light","Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket"]
def get_cart_page(driver, items=ITEMS) -> CartPage:
    login_as_standard_user(driver)
    main_page = MainPage(driver)
    main_page.wait_until_loaded()
    for name in items:
        assert main_page.add_item_to_cart(name), f"Can't add item: {name}"
    main_page.open_cart()
    cart = CartPage(driver)
    cart.wait_until_loaded()
    return cart

@allure.epic("Website")
@allure.feature("Cart")
class TestMain(UiTestCase):
    @allure.story("Open cart page")
    @allure.title("Переход в корзину после добавления товаров")
    def test_open_cart_page(self):
        cart = get_cart_page(self.driver, items=["Sauce Labs Backpack"])
        # Либо wait_until_loaded уже достаточно; если есть is_loaded:
        # self.assertTrue(cart.is_loaded())
        self.assertGreaterEqual(cart.get_items_count(), 1)

    @allure.story("Check items presence")
    @allure.title("Проверка, что все выбранные товары попали в корзину")
    def test_check_items(self):
        cart = get_cart_page(self.driver, items=ITEMS)
        names = cart.get_item_names()
        # сравнение по множеству — устойчиво к изменению порядка
        self.assertSetEqual(set(ITEMS), set(names))
        self.assertEqual(len(ITEMS), cart.get_items_count())

    @allure.story("Remove an item")
    @allure.title("Удаление одного товара из корзины")
    def test_remove_item(self):
        cart = get_cart_page(self.driver, items=ITEMS)
        self.assertTrue(cart.remove_item_by_name("Sauce Labs Bike Light"))
        self.assertEqual(len(ITEMS) - 1, cart.get_items_count())
        self.assertNotIn("Sauce Labs Bike Light", cart.get_item_names())

    @allure.story("Return to main page")
    def test_return_to_main_page(self):
        cart = get_cart_page(self.driver, items=ITEMS)
        pre_count = cart.get_items_count()
        cart.continue_shopping()
        main = MainPage(self.driver)
        main.wait_until_loaded()
        badge = main.get_cart_count()
        self.assertEqual(badge, pre_count)


