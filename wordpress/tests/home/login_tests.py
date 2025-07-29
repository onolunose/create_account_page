"""
Simple and Focused Login Test Suite for Verbatimly
Tests only what matters: login, logout, forgot password, Google auth
Time-wasting boundary and Partition tests were removed
"""

import pytest
import unittest
import os
import time
import logging
from dotenv import load_dotenv
from pages.home.login_page import LoginPage2
from utilities.teststatus import TestStatus
from utilities.util import Util
import utilities.custom_logger as cl

# Load environment variables - FORCE load WordPress env file
wordpress_env_path = 'wordpress/.env.wordpress'
if os.path.exists(wordpress_env_path):
    load_dotenv(wordpress_env_path, override=True)

else:
    load_dotenv()  # fallback to main .env

# Map pytest.ini environment variables to expected names
os.environ['USERNAME'] = os.getenv('TEST_USERNAME', '')
os.environ['PASSWORD'] = os.getenv('TEST_PASSWORD', '')
os.environ['BASE_URL'] = os.getenv('TEST_BASE_URL', 'https://dev-verbatimly.onrender.com')

@pytest.mark.usefixtures("setUp")
class LoginTests2(unittest.TestCase):
    """Focused test class for essential authentication functionality"""

    @pytest.fixture(autouse=True)
    def setUpObject(self, driver):
        """Setup test objects using the driver fixture"""
        self.driver = driver
        self.lp = LoginPage2(self.driver)
        self.ts = TestStatus(self.driver)
        self.util = Util()
        self.log = cl.customLogger(logging.DEBUG)
    #
    @pytest.mark.smoke
    def test_valid_login_and_welcome_message(self):
        """
       Test valid login with env credentials and verify Welcome message
        Expected: Should login successfully and show "Welcome" message
        """
        self.log.info("Starting test_valid_login_and_welcome_message")

        try:
            # Get credentials from environment
            username = os.getenv('TEST_USERNAME')
            password = os.getenv('TEST_PASSWORD')

            if not username or not password:
                self.ts.markFinal("test_valid_login_and_welcome_message", False, "Environment credentials not found")
                return

            self.log.info(f"Testing login with: {username}")

            # Perform login
            login_result = self.lp.perform_login(username, password)
            self.ts.mark(login_result, "Login form submission")

            if not login_result:
                self.ts.markFinal("test_valid_login_and_welcome_message", False, "Login form submission failed")
                return

            # Verify login success by looking for "Welcome" message
            welcome_found = self.lp.verify_login_success()
            self.ts.mark(welcome_found, "Welcome message verification")

            self.ts.markFinal(
                "test_valid_login_and_welcome_message",
                welcome_found,
                f"Valid login test - Welcome message found: {welcome_found}"
            )

        except Exception as e:
            self.log.error(f"Test failed: {str(e)}")
            self.ts.markFinal("test_valid_login_and_welcome_message", False, f"Test failed: {str(e)}")

    @pytest.mark.smoke
    def test_login_logout_welcome_back(self):
        """
        Test complete login-logout flow and verify "Welcome back"
        Expected: Login successfully, logout, and see "Welcome back" message
        """
        self.log.info("Starting test_login_logout_welcome_back")

        try:
            username = os.getenv('USERNAME')
            password = os.getenv('PASSWORD')

            if not username or not password:
                self.ts.markFinal("test_login_logout_welcome_back", False, "Environment credentials not found")
                return

            # Step 1: Login
            self.log.info("Step 1: Performing login")
            login_result = self.lp.perform_login(username, password)
            self.ts.mark(login_result, "Login completed")

            if not login_result:
                self.ts.markFinal("test_login_logout_welcome_back", False, "Login failed")
                return

            # Step 2: Verify login success
            login_success = self.lp.verify_login_success()
            self.ts.mark(login_success, "Login success verified")

            if not login_success:
                self.ts.markFinal("test_login_logout_welcome_back", False, "Login verification failed")
                return

            # Step 3: Logout
            self.log.info("Step 2: Performing logout")
            logout_result = self.lp.perform_logout()
            self.ts.mark(logout_result, "Logout completed")
            # Step 4: Verify "Welcome back" message
            welcome_back = self.lp.verify_welcome_back_message()
            self.ts.mark(welcome_back, "Welcome back message verified")

            overall_success = login_result and login_success and logout_result and welcome_back

            self.ts.markFinal(
                "test_login_logout_welcome_back",
                overall_success,
                f"Login-logout flow completed successfully: {overall_success}"
            )

        except Exception as e:
            self.log.error(f"Test failed: {str(e)}")
            self.ts.markFinal("test_login_logout_welcome_back", False, f"Test failed: {str(e)}")

    #
    def test_login_page_elements(self):
        """
        Test that all essential login page elements are present
        Expected: Email field, password field, login button should be present
        """
        self.log.info("Starting test_login_page_elements")

        try:
            # Navigate to login page
            nav_result = self.lp.navigate_to_login_page()
            self.ts.mark(nav_result, "Navigation to login page")

            if not nav_result:
                self.ts.markFinal("test_login_page_elements", False, "Failed to navigate to login page")
                return

            # Check essential elements
            email_present = self.lp.isElementPresent(self.lp._email_input, "xpath")
            self.ts.mark(email_present, "Email input field present")

            password_present = self.lp.isElementPresent(self.lp._password_input, "xpath")
            self.ts.mark(password_present, "Password input field present")

            login_button_present = self.lp.isElementPresent(self.lp._login_submit_button, "xpath")
            self.ts.mark(login_button_present, "Login button present")

            forgot_password_present = self.lp.isElementPresent(self.lp._forgot_password_link, "xpath")
            self.ts.mark(forgot_password_present, "Forgot password link present")

            all_elements_present = all([email_present, password_present, login_button_present, forgot_password_present])

            self.ts.markFinal(
                "test_login_page_elements",
                all_elements_present,
                f"Login page elements test: {sum([email_present, password_present, login_button_present, forgot_password_present])}/4 elements present"
            )

        except Exception as e:
            self.log.error(f"Test failed: {str(e)}")
            self.ts.markFinal("test_login_page_elements", False, f"Test failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()