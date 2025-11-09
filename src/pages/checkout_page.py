from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

try:
    from selenium.webdriver.support.expected_conditions import any_of  

    HAS_ANY_OF = True
except Exception:
    HAS_ANY_OF = False
import allure

class CheckoutStepOnePage:

    URL_PART = "checkout-step-one"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.checkout_title = (By.CLASS_NAME, "title")
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.zip_code = (By.ID, "postal-code")
        self.btn_continue = (By.ID, "continue")
        self.btn_cancel = (By.ID, "cancel")
        self.error = (By.CSS_SELECTOR, "[data-test='error']")
        self.error_container = (By.CSS_SELECTOR, ".error-message-container.error")

    @allure.step("Wait for the page loading")
    def wait_until_loaded(self, timeout: int = 10):
        w = WebDriverWait(self.driver, timeout)
        w.until(lambda d: "checkout-step-one" in d.current_url or "checkout-step-one.html" in d.current_url)
        w.until(EC.presence_of_element_located(self.first_name))

    @allure.step("Wait for step-one error to appear")
    def wait_for_error(self, timeout: int = 10) -> str | None:
        w = WebDriverWait(self.driver, timeout)
        # Ждём видимость или h3 [data-test='error'] или активный контейнер
        try:
            w.until(
                lambda d: (
                                  len(d.find_elements(*self.error)) > 0
                                  and d.find_elements(*self.error)[0].is_displayed()
                          ) or (
                                  len(d.find_elements(*self.error_container)) > 0
                                  and d.find_elements(*self.error_container)[0].is_displayed()
                          )
            )
        except TimeoutException:
            return None
        return self.get_error_text()  # см. метод ниже

    def get_error_text(self) -> str | None:
        els = self.driver.find_elements(*self.error)
        if els and els[0].is_displayed():
            return els[0].text
        # на всякий — достанем текст из контейнера (если там будет innerText)
        ctn = self.driver.find_elements(*self.error_container)
        if ctn and ctn[0].is_displayed():
            try:
                return ctn[0].text.strip()
            except Exception:
                pass
        return None

    @allure.step("Check if the page is right")
    def is_loaded(self) -> bool:
        return (self.URL_PART in self.driver.current_url
                and len(self.driver.find_elements(*self.first_name)) > 0)

    def _set_input(self, locator, text: str, timeout: int = 15):
        w = WebDriverWait(self.driver, timeout)
        el = w.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        el.click()
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.DELETE)
        if text:
            el.send_keys(text)
            try:
                w.until(lambda d: (el.get_attribute("value") or "").strip() == text)
                return
            except Exception:
                pass
            # JS-fallback (иногда обычный send_keys «съедается» фронтом)
            self.driver.execute_script("""
                    const el = arguments[0], val = arguments[1];
                    el.value = '';
                    el.dispatchEvent(new Event('input', {bubbles:true}));
                    el.value = val;
                    el.dispatchEvent(new Event('input', {bubbles:true}));
                """, el, text)
            w.until(lambda d: (el.get_attribute("value") or "").strip() == text)


    @allure.step("Fill in the form")
    def fill_in_the_form(self,first: str, last: str, zip_code: str):
        self._set_input(self.first_name, first)
        self._set_input(self.last_name, last)
        self._set_input(self.zip_code, zip_code)

    @allure.step("Proceed to payment page")
    def proceed_to_payment(self, timeout: int = 10, require_values: bool = True):
        w = WebDriverWait(self.driver, timeout)

        fn = w.until(EC.visibility_of_element_located(self.first_name))
        ln = w.until(EC.visibility_of_element_located(self.last_name))
        zp = w.until(EC.visibility_of_element_located(self.zip_code))

        if require_values:
            w.until(lambda d: (fn.get_attribute("value") or "").strip())
            w.until(lambda d: (ln.get_attribute("value") or "").strip())
            w.until(lambda d: (zp.get_attribute("value") or "").strip())

        btn = w.until(EC.presence_of_element_located(self.btn_continue))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        try:
            w.until(EC.element_to_be_clickable(self.btn_continue)).click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

        # Гонка условий: либо step-two, либо видимая ошибка на step-one
        def _visible_error(d):
            es = d.find_elements(*self.error)
            if es and es[0].is_displayed():
                return True
            cs = d.find_elements(*self.error_container)
            return bool(cs and cs[0].is_displayed())

        try:
            w.until(lambda d: "checkout-step-two" in d.current_url or _visible_error(d))
        except TimeoutException:
            with allure.step(f"Proceed failed | url={self.driver.current_url}"):
                allure.attach(self.driver.page_source, "DOM", allure.attachment_type.HTML)
            raise

    @allure.step("Wait for step-one error to appear")
    def wait_for_error(self, timeout: int = 10) -> str | None:
        w = WebDriverWait(self.driver, timeout)

        def _visible_text():
            es = self.driver.find_elements(*self.error)
            if es and es[0].is_displayed():
                return es[0].text.strip()
            cs = self.driver.find_elements(*self.error_container)
            if cs and cs[0].is_displayed():
                try:
                    return cs[0].text.strip()
                except Exception:
                    return None
            return None

        try:
            return w.until(lambda d: _visible_text())
        except TimeoutException:
            return None

    @allure.step("Cancel your order")
    def cancel_checkout(self):
        self.driver.find_element(*self.btn_cancel).click()

    @allure.step("Get error message")
    def get_error_text(self) -> str | None:
        try:
            return self.driver.find_element(*self.error).text
        except NoSuchElementException:
            return None

class CheckoutStepTwoPage:

    URL_PART = "checkout-step-two"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.checkout_title = (By.CLASS_NAME, "title")
        self.item_names = (By.CLASS_NAME, "inventory_item_name")
        self.subtotal = (By.CLASS_NAME, "summary_subtotal_label")
        self.tax = (By.CLASS_NAME, "summary_tax_label")
        self.total = (By.CLASS_NAME, "summary_total_label")
        self.btn_finish = (By.ID, "finish")
        self.btn_cancel = (By.ID, "cancel")

    def wait_until_loaded(self, timeout: int = 10):
        w = WebDriverWait(self.driver, timeout)
        w.until(lambda d: "checkout-step-two" in d.current_url or "checkout-step-two.html" in d.current_url)
        w.until(EC.presence_of_element_located(self.subtotal))  # уникальный элемент обзора

    def is_loaded(self) -> bool:
        return self.URL_PART in self.driver.current_url

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.driver.find_elements(*self.item_names)]

    def _extract_money(self, text: str) -> float:
        return float(text.split("$")[-1])

    def get_subtotal(self) -> float:
        return self._extract_money(self.driver.find_element(*self.subtotal).text)

    @allure.step("Finish checkout")
    def finish(self, timeout: int = 10):
        w = WebDriverWait(self.driver, timeout)
        btn = w.until(EC.presence_of_element_located(self.btn_finish))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        w.until(EC.element_to_be_clickable(self.btn_finish)).click()
        w.until(lambda d: "checkout-complete" in d.current_url or "checkout-complete.html" in d.current_url)

    @allure.step("Cancel from overview")
    def cancel(self, timeout: int = 10):
        wait = WebDriverWait(self.driver, timeout)
        btn = wait.until(EC.presence_of_element_located(self.btn_cancel))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        wait.until(EC.element_to_be_clickable(self.btn_cancel)).click()
        # SauceDemo: Cancel returns us back to inventory page
        wait.until(lambda d: "inventory" in d.current_url)

class CheckoutCompletePage:

    URL_PART = "checkout-complete"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.complete_header = (By.CLASS_NAME, "complete-header")
        self.btn_back_home = (By.ID, "back-to-products")

    def is_loaded(self, timeout: int = 10) -> bool:
        w = WebDriverWait(self.driver, timeout)
        w.until(lambda d: "checkout-complete" in d.current_url or "checkout-complete.html" in d.current_url)
        w.until(EC.presence_of_element_located(self.complete_header))
        return True

    def get_header_text(self) -> str:
        return self.driver.find_element(*self.complete_header).text