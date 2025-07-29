# base/basepage.py
from base.selenium_driver import SeleniumDriver
from utilities.util import Util

class BasePage(SeleniumDriver):
    def __init__(self, driver, explicit_wait_seconds=20, screenshots_dir="screenshots"):
        super().__init__(driver, explicit_wait_seconds, screenshots_dir)
        self.util = Util()

    def verifyPageTitle(self, titleToVerify: str):
        try:
            actual = self.getTitle()
            return self.util.verifyTextContains(actual, titleToVerify)
        except Exception:
            self.log.error("Failed to get/verify page title")
            self.screenShot("verify_title_error")
            return False
