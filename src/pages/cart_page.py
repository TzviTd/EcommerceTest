from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class CartPage:
    """Page Object для корзины (cart page) после логина."""

    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.cart_title = (By.CLASS_NAME, "title")
        self.cart_items = (By.CLASS_NAME, "cart_item")
        self.items_table = (By.CLASS_NAME, "cart_item")
        self.item_name = (By.CLASS_NAME, "inventory_item_name")
        self.item_price = (By.CLASS_NAME, "inventory_item_price")
        self.return_to_main = (By.ID, "continue-shopping")
        self.btn_checkout = (By.ID, "checkout")
        self.btn_remove_in_item = (By.XPATH, ".//button[contains(@id,'remove') or normalize-space()='Remove']")

    @allure.step("Wait for the page loading")
    def wait_until_loaded(self, timeout: int = 10):
        w = WebDriverWait(self.driver, timeout)
        w.until(lambda d: "cart" in d.current_url or "cart.html" in d.current_url)
        # На некоторых стендах .cart_item может быть пустым — ждём checkout-кнопку
        w.until(EC.presence_of_element_located(self.btn_checkout))

    @allure.step("Check if the page is right")
    def is_loaded(self) -> bool:
        return "cart" in self.driver.current_url

    @allure.step("Get items list")
    def get_item_names(self):
        items = self.driver.find_elements(*self.cart_items)
        names = []
        for row in items:
            name_el = row.find_element(*self.item_name)
            names.append(name_el.text)
        return names

    @allure.step("Get items prices")
    def get_item_prices(self):
        items = self.driver.find_elements(*self.cart_items)
        prices = []
        for row in items:
            price_el = row.find_element(*self.item_price)
            prices.append(float(price_el.text.replace("$", "").strip()))
        return prices

    @allure.step("Get cart items count")
    def get_items_count(self) -> int:
        return len(self.driver.find_elements(*self.cart_items))

    @allure.step("Remove item from cart by name: {name}")
    def remove_item_by_name(self, name: str, timeout: int = 8) -> bool:
        """Удаляет товар по имени. Возвращает True, если нашли и удалили."""
        # 1) Items' locator
        row_by_name = (
            By.XPATH,
            f"//div[contains(@class,'cart_item')]"
            f"[.//div[contains(@class,'inventory_item_name') and normalize-space()=\"{name}\"]]"
        )

        wait = WebDriverWait(self.driver, timeout)

        try:
            # making sure the row has appeared
            row = wait.until(EC.presence_of_element_located(row_by_name))
        except TimeoutException:
            return False

        before = self.get_items_count()

        # 2) Click Remove inside the row
        try:
            btn = row.find_element(*self.btn_remove_in_item)
            # на всякий случай проскроллим, чтобы избежать перекрытий
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            wait.until(EC.element_to_be_clickable(self.btn_remove_in_item))  # в пределах row обычно достаточно
            btn.click()
        except Exception:
            return False

        # 3) Waiting the row to disappear
        try:
            wait.until(EC.invisibility_of_element_located(row_by_name))
            return True
        except TimeoutException:
            # fallback
            try:
                wait.until(lambda d: len(d.find_elements(*self.cart_items)) == before - 1)
                return True
            except TimeoutException:
                return False

    @allure.step("Go back to main page")
    def continue_shopping(self):
        self.driver.find_element(*self.return_to_main).click()

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self, timeout: int = 12):
        w = WebDriverWait(self.driver, timeout)
        if "cart" not in self.driver.current_url:
            try:
                from src.pages.main_page import MainPage
                MainPage(self.driver).open_cart(timeout=timeout)
            except Exception:
                self.driver.get("https://www.saucedemo.com/cart.html")
        # going on, click on checkout
        btn = w.until(EC.presence_of_element_located(self.btn_checkout))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        w.until(EC.element_to_be_clickable(self.btn_checkout)).click()
        w.until(lambda d: "checkout-step-one" in d.current_url or "checkout-step-one.html" in d.current_url)