import os
import unittest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class UiTestCase(unittest.TestCase):
    """
    Базовый TestCase:
      - Переключаемый headless/visible режим через ENV HEADLESS
      - Стабильные флаги для headless
      - Единый window-size
      - page_load_timeout и нулевой implicit wait (используем явные ожидания)
      - Скриншот в Allure при падении (до закрытия браузера)
    """

    def setUp(self):
        headless = os.getenv("HEADLESS", "true").lower() == "true"

        opts = Options()

        # 🔒 disable password manager / save-password bubble / autofill / onboarding
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
            # иногда помогает отключение подсказок по логинам:
            "credentials_enable_autosignin": False,
        }
        opts.add_experimental_option("prefs", prefs)
        opts.add_argument("--incognito")  # чистый профиль без сохранённых паролей
        opts.add_argument("--no-first-run")
        opts.add_argument("--no-default-browser-check")
        opts.add_argument("--disable-notifications")
        opts.add_argument("--disable-popup-blocking")
        # ключевые фичи Chrome, отключающие подсказки/онбординги
        opts.add_argument(
            "--disable-features=Autofill,AutofillServerCommunication,AutofillTypeSpecificFeatures,PasswordManagerOnboarding,AccountConsistency,PrivacySandboxSettings4")

        # универсальные флаги
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")

        if headless:
            # Новый движок headless у Chromium
            opts.add_argument("--headless=new")
            # фиксированный и достаточно большой вьюпорт
            opts.add_argument("--window-size=1920,1080")
            # мелкие «анти-флейк» тюнинги
            opts.add_argument("--force-device-scale-factor=1")
            opts.add_argument("--hide-scrollbars")
            opts.add_argument("--disable-dev-shm-usage")
        else:
            # видимый режим
            opts.add_argument("--start-maximized")
            opts.add_argument("--window-size=1600,1000")

        self.driver = webdriver.Chrome(options=opts)
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(0)  # всегда только явные ожидания

    def tearDown(self):
        # если тест упал — приложим скрин до закрытия браузера
        failed = False
        outcome = getattr(self, "_outcome", None)
        if outcome:
            result = getattr(outcome, "result", None) or outcome
            errors = getattr(result, "errors", []) or []
            failures = getattr(result, "failures", []) or []
            failed = any(e for _, e in errors + failures)

        if failed:
            try:
                png = self.driver.get_screenshot_as_png()
                allure.attach(png, name=self.id(), attachment_type=allure.attachment_type.PNG)
                # опционально URL/DOM (включай по необходимости)
                allure.attach(self.driver.current_url, "URL", allure.attachment_type.TEXT)
                # allure.attach(self.driver.page_source, "DOM", allure.attachment_type.HTML)
            except Exception:
                pass  # не ломаем teardown

        try:
            self.driver.quit()
        except Exception:
            pass
