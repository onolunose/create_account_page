import utilities.custom_logger as cl
import logging
from base.selenium_driver import SeleniumDriver
from traceback import print_stack


class TestStatus(SeleniumDriver):
    log = cl.customLogger(logging.INFO)

    def __init__(self, driver):
        """
        Initialize TestStatus class with driver instance and an empty result list.

        Args:
        - driver: WebDriver instance.
        """
        super(TestStatus, self).__init__(driver)
        self.driver = driver
        self.resultList = []

    def setResult(self, result, resultMessage):
        """
        Set the test result and log the appropriate message.

        Args:
        - result (bool): Test result (True for pass, False for fail).
        - resultMessage (str): Message to log.
        """
        try:
            if result is not None:
                if result:
                    self.resultList.append("PASS")
                    self.log.info(f"### VERIFICATION SUCCESSFUL: {resultMessage}")
                else:
                    self.resultList.append("FAIL")
                    self.log.error(f"### VERIFICATION FAILED: {resultMessage}")
                    self.screenShot(resultMessage)
            else:
                self.resultList.append("FAIL")
                self.log.error(f"### VERIFICATION FAILED: {resultMessage}")
                self.screenShot(resultMessage)
        except:
            self.resultList.append("FAIL")
            self.log.error("### An Exception Occurred!")
            self.screenShot(resultMessage)
            print_stack()

    def mark(self, result, resultMessage):
        """
        Mark the result of a verification point in a test case.

        Args:
        - result (bool): Test result (True for pass, False for fail).
        - resultMessage (str): Message to log.
        """
        self.setResult(result, resultMessage)

    def markFinal(self, testName, result, resultMessage):
        """
        Mark the final result of a verification point in a test case.
        This method should be called at least once in a test case to determine the final status.

        Args:
        - testName (str): Name of the test.
        - result (bool): Test result (True for pass, False for fail).
        - resultMessage (str): Message to log.
        """
        self.setResult(result, resultMessage)

        if "FAIL" in self.resultList:
            self.log.error(f"{testName} - TEST FAILED")
            self.resultList.clear()
            assert False
        else:
            self.log.info(f"{testName} - TEST PASSED SUCCESSFULLY")
            self.resultList.clear()
            assert True
