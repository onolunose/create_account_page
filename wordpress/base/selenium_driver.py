# base/selenium_driver.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from utilities.custom_logger import customLogger
from pathlib import Path
import time
import os

class SeleniumDriver:
    def __init__(self, driver, explicit_wait_seconds: int = 20, screenshots_dir: str = "screenshots"):
        self.driver = driver
        self.log = customLogger("selenium")
        self._wait_s = explicit_wait_seconds
        self._screens_dir = Path(screenshots_dir)

    # ---------- Utilities ----------
    def screenShot(self, name: str):
        self._screens_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{name}.{int(time.time()*1000)}.png"
        path = self._screens_dir / file_name
        self.driver.save_screenshot(str(path))
        self.log.info("📸 Screenshot: %s", path)
        return str(path)

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType: str):
        lt = (locatorType or "").lower()
        return {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME,
            "link": By.LINK_TEXT
        }.get(lt, None)

    def getElement(self, locator, locatorType="id"):
        try:
            byType = self.getByType(locatorType)
            el = self.driver.find_element(byType, locator)
            return el
        except Exception as e:
            self.log.error("getElement failed: %s (%s)", locator, locatorType)
            return None

    def getElementList(self, locator, locatorType="id"):
        try:
            byType = self.getByType(locatorType)
            return self.driver.find_elements(byType, locator)
        except Exception:
            return []

    # ---------- Waits ----------
    def wait_clickable(self, locator, locatorType="id", timeout=None):
        byType = self.getByType(locatorType)
        wait = WebDriverWait(self.driver, timeout or self._wait_s,
                             poll_frequency=0.5,
                             ignored_exceptions=[NoSuchElementException,
                                                 ElementNotVisibleException,
                                                 ElementNotSelectableException])
        return wait.until(EC.element_to_be_clickable((byType, locator)))

    def wait_visible(self, locator, locatorType="id", timeout=None):
        byType = self.getByType(locatorType)
        wait = WebDriverWait(self.driver, timeout or self._wait_s)
        return wait.until(EC.visibility_of_element_located((byType, locator)))

    def wait_present(self, locator, locatorType="id", timeout=None):
        byType = self.getByType(locatorType)
        wait = WebDriverWait(self.driver, timeout or self._wait_s)
        return wait.until(EC.presence_of_element_located((byType, locator)))

    def wait_url_contains(self, fragment: str, timeout=None):
        wait = WebDriverWait(self.driver, timeout or self._wait_s)
        return wait.until(EC.url_contains(fragment))

    # ---------- Actions ----------
    def elementClick(self, locator="", locatorType="id", element=None):
        try:
            el = element or self.wait_clickable(locator, locatorType)
            el.click()
        except Exception as e:
            self.log.error("Click failed on %s (%s)", locator, locatorType)
            self.screenShot("click_failed")
            raise

    def sendKeys(self, data, locator="", locatorType="id", element=None, clear_first=True):
        try:
            el = element or self.wait_visible(locator, locatorType)
            if clear_first:
                el.clear()
            el.send_keys(data)
        except Exception:
            self.log.error("sendKeys failed on %s (%s)", locator, locatorType)
            self.screenShot("sendkeys_failed")
            raise

    def getText(self, locator="", locatorType="id", element=None):
        el = element or self.wait_visible(locator, locatorType)
        txt = (el.text or el.get_attribute("innerText") or "").strip()
        return txt

    def isElementPresent(self, locator="", locatorType="id", element=None):
        try:
            el = element or self.getElement(locator, locatorType)
            return el is not None
        except Exception:
            return False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        try:
            el = element or self.getElement(locator, locatorType)
            return el.is_displayed() if el else False
        except Exception:
            return False

    def webScroll(self, direction="up", amount=1000):
        y = -abs(amount) if direction == "up" else abs(amount)
        self.driver.execute_script(f"window.scrollBy(0, {y});")

    def quitter(self):
        self.driver.quit()
