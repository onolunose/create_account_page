from pages.home.login_page import LoginPage
from utilities.teststatus import TestStatus
import unittest
import pytest
import utilities.custom_logger as cl
import logging


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class LoginTests(unittest.TestCase):
    log = cl.customLogger(logging.DEBUG)
    #@pytest.mark.skip
    #@pytest.mark.first
    @pytest.fixture(autouse=True)
    def setUpObject(self, oneTimeSetUp):
        """
        Setup objects for the test class.

        Args:
        - oneTimeSetUp: Fixture for setting up WebDriver instance.
        """
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    @pytest.mark.skip
    @pytest.mark.run(order=2)
    def test_logout(self):
        # self.lp.login("abcdetest@gmail.com", "abc123ABC")
        self.lp.createAccountPage("ekIOitiibddifaith204376ttyhjy@gmail.com", "###ghwaabcgh123tyJKXYZ$$78", "uieghkiHHkigrptiibifaith204376")

        self.lp.logout()
        result3 = self.lp.verifyLogoutSuccessful()
        print("Result3: " + str(result3))
        self.ts.markFinal("test_invalidLogout", result3, "Logout Successful")
        self.driver.quit()

    @pytest.mark.skip
    @pytest.mark.run(order=1)
    def test_validAccount(self):
        """
        Test case to verify valid login functionality.
        """
        self.log.info("*##" * 30)
        self.log.info("test_validLogin started")
        self.log.info("*##" * 30)

        # Login with valid credentials and then logout
        # self.lp.logout()
        self.lp.createAccountPage("ifaith20437MMMd45fe6ty@gmail.com", "###waabc123X78KOOPYZfgh$$78", "uiekiMHGTtiopl23ibifaith204376")



        #Verify successful login
        result1 = self.lp.verifyAccountSuccessful()
        result2 = self.lp.verifyAccountSuccessful2()

        # Mark the results for reporting
        print("Result1: " + str(result1))
        print("Result2: " + str(result2))
        self.ts.mark(result2, "Create Account Verification Successful")
        #self.driver.quit()

    @pytest.mark.skip
    @pytest.mark.run(order=3)
    def test_invalidAccountEmptyFields(self):
        """
        Test case to verify invalid login functionality.
        """
        self.log.info("*##" * 30)
        self.log.info("test_invalidAccountEmptyFields(")
        self.log.info("*##" * 30)

        # Login with valid credentials and then logout
        # self.lp.logout()
        self.lp.createAccountPage("", "", "")

        # Verify successful login
        result1 = self.lp.verifyinvalidAccountEmptyEmailSuccessful()
        result2 = self.lp.verifyinvalidAccountEmptyUsernameSuccessful()
        result3 = self.lp.verifyinvalidAccountEmptyPasswordSuccessful()

        # Mark the results for reporting
        print("Result1: " + str(result1))
        print("Result2: " + str(result2))
        print("Result3: " + str(result2))
        self.ts.mark(result1, "Email Invalid Verification Successful")
        self.ts.mark(result2, "User name Invalid Verification Successful")
        self.ts.mark(result3, "Password Invalid Verification Successful")
        self.driver.quit()

    #@pytest.mark.skip
    @pytest.mark.run(order=3)
    def test_invalidAccountNullFields(self):
        """
        Test case to verify invalid login functionality.
        """
        self.log.info("*##" * 30)
        self.log.info("test_invalidAccountEmptyFields(")
        self.log.info("*##" * 30)

        # Login with valid credentials and then logout
        # self.lp.logout()
        self.lp.createAccountPage2(email=None, username=None, password=None)

        # Verify successful login
        result1 = self.lp.verifyinvalidAccountNullEmailSuccessful()
        result2 = self.lp.verifyinvalidAccountNullUsernameSuccessful()
        result3 = self.lp.verifyinvalidAccountNullPasswordSuccessful()

        # Mark the results for reporting
        print("Result1: " + str(result1))
        print("Result2: " + str(result2))
        print("Result3: " + str(result2))
        self.ts.mark(result1, "Email Invalid Verification Successful")
        self.ts.mark(result2, "User name Invalid Verification Successful")
        self.ts.mark(result3, "Password Invalid Verification Successful")
        self.ts.markFinal("Validate Null Value",result3, "Null Value Verification")
        self.driver.quit()


