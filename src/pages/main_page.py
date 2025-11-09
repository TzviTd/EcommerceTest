from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class MainPage:

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Locators
        self.inventory_item = (By.CLASS_NAME, "inventory_item")
        self.item_name = (By.CLASS_NAME, "inventory_item_name")
        self.cart_link = (By.CLASS_NAME, "shopping_cart_link")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.menu_button = (By.ID, "react-burger-menu-btn")
        self.logout_link = (By.ID, "logout_sidebar_link")

    @allure.step("Waiting inventory")
    def wait_until_loaded(self, timeout: int = 10):
        """Waiting for a least the first item to appear"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.inventory_item)
        )

    @allure.step("Checking if we are on inventory page")
    def is_loaded(self) -> bool:
        return "inventory" in self.driver.current_url

    @allure.step("Getting the full items list")
    def get_item_names(self):
        items = self.driver.find_elements(*self.item_name)
        return [el.text for el in items]

    @allure.step("Adding the item to cart")
    def add_item_to_cart(self, name: str):
        items = self.driver.find_elements(*self.inventory_item)
        for item in items:
            if name in item.text:
                button = item.find_element(By.TAG_NAME, "button")
                button.click()
                return True
        return False

    @allure.step("Passing to the cart")
    def open_cart(self, timeout: int = 12):
        w = WebDriverWait(self.driver, timeout)
        link = w.until(EC.presence_of_element_located(self.cart_link))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
        w.until(EC.element_to_be_clickable(self.cart_link)).click()
        w.until(lambda d: "cart" in d.current_url or "cart.html" in d.current_url)

    @allure.step("Checking the number of items")
    def get_cart_count(self) -> int:
        try:
            badge = self.driver.find_element(*self.cart_badge)
            return int(badge.text)
        except Exception:
            return 0

    @allure.step("Logging out")
    def logout(self):
        self.driver.find_element(*self.menu_button).click()
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.logout_link)
        )
        self.driver.find_element(*self.logout_link).click()




