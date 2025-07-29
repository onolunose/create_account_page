"""
Login Page Object for Verbatimly - Authentication Testing
Covers login, logout, password reset, and Google authentication
"""

import logging
from base.basepage import BasePage
from utilities.util import Util
import utilities.custom_logger as cl
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class LoginPage2(BasePage):
    """Enhanced page object for Verbatimly authentication functionality"""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.log = cl.customLogger(logging.DEBUG)
        self.util = Util()

    # NAVIGATION LOCATORS (From Login Page HTML)
    _verbatimly_logo = "//span[text()='Verbatimly']"
    _back_to_home_button = "//button[contains(text(), 'Back to home')]"
    _back_to_signin_button = "//a[contains(text(), 'Back to sign in')] | //button[contains(text(), 'Back to sign in')]"

    # MAIN PAGE LOCATORS
    _start_for_free_button = "//button[contains(text(), 'Start for free')] | //a[contains(text(), 'Start for free')]"
    _sign_in_button = "//button[contains(text(), 'Sign in')] | //button[contains(text(), 'Sign up')]"

    # LOGIN FORM LOCATORS
    _email_input = "//input[@id='email']"
    _email_input_alt = "//input[@name='email']"
    _password_input = "//input[@id='password']"
    _password_input_alt = "//input[@name='password']"
    _remember_me_checkbox = "//input[@type='checkbox']"
    _login_submit_button = "//button[@type='submit']"

    # PASSWORD VISIBILITY TOGGLE
    _password_toggle = "//input[@id='password']//following-sibling::button"
    _password_eye_icon = "//button[.//*[contains(@class, 'lucide-eye')]]"

    # GOOGLE AUTHENTICATION
    _google_login_button = "//button[contains(., 'Google')]"
    _google_button_svg = "//button//span[text()='Google']"

    # FORGOT PASSWORD
    _forgot_password_link = "//a[@href='/auth/forgot-password']"
    _forgot_password_text = "//a[text()='Forgot password?']"
    _reset_email_input = "//input[@type='email']"
    _send_reset_link_button = "//button[.//span[normalize-space()='Send reset link']]"

    # SUCCESS/ERROR INDICATORS
    _welcome_message = "//*[contains(text(), 'Welcome')] | //h1[contains(text(), 'Welcome')]"
    _welcome_back_message = "//h1[text()='Welcome back']"
    _check_your_email_message = "//*[contains(text(), 'Check your email')] | //h1[contains(text(), 'Check your email')]"
    _dashboard_indicator = "//*[contains(text(), 'Dashboard')] | //*[contains(text(), 'Total Files')] | //*[contains(text(), 'Manage your transcriptions')]"

    # USER PROFILE AND LOGOUT
    _user_profile_button = "//div[normalize-space(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))='free plan']"
    _user_dropdown_button = "//div[text()='TO']"
    _user_initials_button = "//div[text()='TO'] | //button[contains(text(), 'TO')] | //div[contains(@class, 'avatar')]"
    _profile_menu_button = "//button[.//*[contains(@class, 'profile')]] | //div[contains(@class, 'user-avatar')]"
    _sign_out_button = "//button[contains(text(), 'Sign out')] | //a[contains(text(), 'Sign out')] | //*[contains(text(), 'Logout')]"

    # VALIDATION MESSAGES
    _error_message = "//div[contains(@class, 'error')] | //span[contains(@class, 'error')] | //*[contains(@class, 'alert')]"
    _validation_message = "//div[contains(@class, 'validation')] | //span[contains(@class, 'invalid')]"

    # PAGE TITLES AND HEADINGS
    _page_title = "//h1 | //h2 | //title"
    _login_heading = "//h1[contains(text(), 'Sign in')] | //h2[contains(text(), 'Login')] | //h1[contains(text(), 'Welcome back')]"

    # NAVIGATION METHODS
    def navigate_to_main_page(self):
        """Navigate to the main application page"""
        try:
            main_url = os.getenv('BASE_URL', 'https://dev-verbatimly.onrender.com')
            self.driver.get(main_url)
            self.util.sleep(3)
            self.log.info(f"Navigated to main page: {main_url}")
            return True
        except Exception as e:
            self.log.error(f"Error navigating to main page: {str(e)}")
            return False

    def navigate_to_login_page(self):
        """Navigate to login page via Sign In button"""
        try:
            # First go to main page
            if not self.navigate_to_main_page():
                return False

            # Look for and click Sign In button
            if self.isElementPresent(self._sign_in_button, "xpath"):
                self.elementClick(self._sign_in_button, "xpath")
                self.util.sleep(2)
                self.log.info("Clicked Sign In button")
                return True
            else:
                # Try direct navigation to login URL
                login_url = f"{os.getenv('BASE_URL', 'https://dev-verbatimly.onrender.com')}/auth/login"
                self.driver.get(login_url)
                self.util.sleep(2)
                self.log.info(f"Direct navigation to login page: {login_url}")
                return True
        except Exception as e:
            self.log.error(f"Error navigating to login page: {str(e)}")
            return False

    def navigate_to_forgot_password_page(self):
        """Navigate to forgot password page """
        try:
            if not self.navigate_to_login_page():
                return False

            if self.isElementPresent(self._forgot_password_link, "xpath"):
                self.elementClick(self._forgot_password_link, "xpath")
                self.util.sleep(2)
                self.log.info("Navigated to forgot password page using href")
                return True
            # Fallback using text
            elif self.isElementPresent(self._forgot_password_text, "xpath"):
                self.elementClick(self._forgot_password_text, "xpath")
                self.util.sleep(2)
                self.log.info("Navigated to forgot password page using text")
                return True
            else:
                self.log.error("Forgot password link not found")
                return False
        except Exception as e:
            self.log.error(f"Error navigating to forgot password page: {str(e)}")
            return False

    # ClearFIELD
    def clear_field_safely(self, locator, locator_type="xpath"):
        """Safely clear a field with multiple methods"""
        try:
            element = self.getElement(locator, locator_type)
            if element:
                # Method 1: Select all and delete
                element.click()
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.DELETE)
                time.sleep(0.2)

                # Method 2: Clear if still has content
                if element.get_attribute('value'):
                    element.clear()
                    time.sleep(0.2)

                # Method 3: Backspace if still has content
                current_value = element.get_attribute('value')
                if current_value:
                    for _ in range(len(current_value)):
                        element.send_keys(Keys.BACKSPACE)
                        time.sleep(0.1)

                self.log.info("Field cleared successfully")
                return True
        except Exception as e:
            self.log.error(f"Error clearing field: {str(e)}")
            return False

    def enter_email(self, email):
        """Enter email address with field clearing"""
        try:
            # Primary locator
            if self.isElementPresent(self._email_input, "xpath"):
                self.clear_field_safely(self._email_input)
                self.sendKeys(email, self._email_input, "xpath")
                self.log.info(f"Entered email: {email}")
                return True
            # Fallback locator for self healing
            elif self.isElementPresent(self._email_input_alt, "xpath"):
                self.clear_field_safely(self._email_input_alt)
                self.sendKeys(email, self._email_input_alt, "xpath")
                self.log.info(f"Entered email: {email}")
                return True
            else:
                self.log.error("Email input field not found")
                return False
        except Exception as e:
            self.log.error(f"Error entering email: {str(e)}")
            return False

    def enter_password(self, password):
        """Enter password with field clearing """
        try:
            # Primary locator
            if self.isElementPresent(self._password_input, "xpath"):
                self.clear_field_safely(self._password_input)
                self.sendKeys(password, self._password_input, "xpath")
                self.log.info("Entered password")
                return True
            # Fallback locator self healing
            elif self.isElementPresent(self._password_input_alt, "xpath"):
                self.clear_field_safely(self._password_input_alt)
                self.sendKeys(password, self._password_input_alt, "xpath")
                self.log.info("Entered password")
                return True
            else:
                self.log.error("Password input field not found")
                return False
        except Exception as e:
            self.log.error(f"Error entering password: {str(e)}")
            return False

    def check_remember_me(self):
        """Check the remember me checkbox if present"""
        try:
            if self.isElementPresent(self._remember_me_checkbox, "xpath"):
                checkbox = self.getElement(self._remember_me_checkbox, "xpath")
                if checkbox and not checkbox.is_selected():
                    self.elementClick(self._remember_me_checkbox, "xpath")
                    self.log.info("Checked remember me checkbox")
                return True
            return True  # Not required, so return True
        except Exception as e:
            self.log.error(f"Error with remember me checkbox: {str(e)}")
            return True  # Not critical, continue

    def click_login_button(self):
        """Click the login/sign in button"""
        try:
            if self.isElementPresent(self._login_submit_button, "xpath"):
                self.elementClick(self._login_submit_button, "xpath")
                self.util.sleep(3)  # Wait for login processing
                self.log.info("Clicked login button")
                return True
            else:
                self.log.error("Login button not found")
                return False
        except Exception as e:
            self.log.error(f"Error clicking login button: {str(e)}")
            return False

    # COMPLETE LOGIN FLOW
    def perform_login(self, email, password, remember_me=False):
        """Complete login flow with credentials"""
        try:
            self.log.info(f"Starting login process for: {email}")

            # Navigate to login page
            if not self.navigate_to_login_page():
                return False

            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self._email_input))
            )

            # Enter credentials
            if not self.enter_email(email):
                return False

            if not self.enter_password(password):
                return False

            # Check remember me if requested
            if remember_me:
                self.check_remember_me()

            # Submit login
            if not self.click_login_button():
                return False

            self.log.info("Login process completed")
            return True

        except Exception as e:
            self.log.error(f"Error in login process: {str(e)}")
            return False

    def login_with_env_credentials(self):
        """Login using credentials from environment variables"""
        try:
            username = os.getenv('USERNAME')
            password = os.getenv('PASSWORD')

            if not username or not password:
                self.log.error("Username or password not found in environment variables")
                return False

            return self.perform_login(username, password)

        except Exception as e:
            self.log.error(f"Error logging in with env credentials: {str(e)}")
            return False

    # GOOGLE AUTHENTICATION
    def click_google_login(self):
        """Click Google login button - using exact HTML structure"""
        try:
            # Primary selector based on actual HTML structure
            if self.isElementPresent(self._google_login_button, "xpath"):
                self.elementClick(self._google_login_button, "xpath")
                self.util.sleep(3)
                self.log.info("Clicked Google login button")
                return True
            # Alternative selector
            elif self.isElementPresent(self._google_button_svg, "xpath"):
                # Click parent button of the span
                self.elementClick("//button[.//span[text()='Google']]", "xpath")
                self.util.sleep(3)
                self.log.info("Clicked Google login button (alternative)")
                return True
            else:
                self.log.error("Google login button not found")
                return False
        except Exception as e:
            self.log.error(f"Error clicking Google login: {str(e)}")
            return False

    def handle_google_authentication(self):
        """Handle Google authentication flow"""
        try:
            if not self.navigate_to_login_page():
                return False

            if not self.click_google_login():
                return False

            # Wait for Google login page or redirect
            self.util.sleep(5)

            # Check if Google login window opened
            current_url = self.driver.current_url
            if "google" in current_url.lower() or "accounts.google.com" in current_url:
                self.log.info("Google authentication page loaded")

                # Clear and enter Google email if field is present
                google_email_selectors = [
                    "//input[@type='email']",
                    "//input[@id='identifierId']",
                    "//input[@name='identifier']"
                ]

                for selector in google_email_selectors:
                    if self.isElementPresent(selector, "xpath"):
                        self.clear_field_safely(selector)
                        username = os.getenv('USERNAME')
                        if username:
                            self.sendKeys(username, selector, "xpath")
                            self.log.info("Entered Google email")
                        break

                return True
            else:
                self.log.info("Google authentication may have completed or failed")
                return True

        except Exception as e:
            self.log.error(f"Error in Google authentication: {str(e)}")
            return False

    # FORGOT PASSWORD FUNCTIONALITY
    def request_password_reset(self, email):
        """Request password reset for given email"""
        try:
            if not self.navigate_to_forgot_password_page():
                return False

            # Wait for forgot password page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self._reset_email_input))
            )

            # Clear and enter email
            self.clear_field_safely(self._reset_email_input)
            self.sendKeys(email, self._reset_email_input, "xpath")
            self.log.info(f"Entered email for password reset: {email}")

            # Click send reset link
            if self.isElementPresent(self._send_reset_link_button, "xpath"):
                self.elementClick(self._send_reset_link_button, "xpath")
                self.util.sleep(3)
                self.log.info("Clicked send reset link button")
                return True
            else:
                self.log.error("Send reset link button not found")
                return False

        except Exception as e:
            self.log.error(f"Error requesting password reset: {str(e)}")
            return False

    def request_password_reset_with_env_email(self):
        """Request password reset using email from environment"""
        try:
            email = os.getenv('USERNAME')
            if not email:
                self.log.error("Email not found in environment variables")
                return False

            return self.request_password_reset(email)

        except Exception as e:
            self.log.error(f"Error requesting password reset with env email: {str(e)}")
            return False

    # LOGOUT FUNCTIONALITY - UPDATED BASED ON SCREENSHOTS
    def click_user_profile_menu(self):
        """Click user profile/dropdown menu - Updated for TO button with gradient"""
        try:
            # Primary selector
            if self.isElementPresent(self._user_profile_button, "xpath"):
                self.elementClick(self._user_profile_button, "xpath")
                self.util.sleep(3)  # Wait 3 seconds as specified
                self.log.info("Clicked user profile menu (gradient TO button)")
                return True

            # Fallback selector (self healing)
            elif self.isElementPresent(self._user_dropdown_button, "xpath"):
                self.elementClick(self._user_dropdown_button, "xpath")
                self.util.sleep(3)  # Wait 3 seconds as specified
                self.log.info("Clicked user profile menu (TO text)")
                return True

            # Additional fallback selectors (self healing)
            elif self.isElementPresent(self._user_initials_button, "xpath"):
                self.elementClick(self._user_initials_button, "xpath")
                self.util.sleep(3)  # Wait 3 seconds as specified
                self.log.info("Clicked user profile menu (initials button)")
                return True

            else:
                self.log.error("User profile menu not found")
                return False

        except Exception as e:
            self.log.error(f"Error clicking user profile menu: {str(e)}")
            return False
    def click_sign_out(self):
        """Click sign out button - with scroll down to find it"""
        try:
            # Wait for dropdown to be fully loaded
            self.util.sleep(1)

            if self.isElementPresent(self._sign_out_button, "xpath"):
                # Scroll the sign out button into view
                sign_out_element = self.getElement(self._sign_out_button, "xpath")
                if sign_out_element:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", sign_out_element)
                    self.util.sleep(1)

                    # Click the sign out button
                    self.elementClick(self._sign_out_button, "xpath")
                    self.util.sleep(3)
                    self.log.info("Clicked sign out button")
                    return True
                else:
                    self.log.error("Sign out element found but could not get element object")
                    return False
            else:
                self.log.error("Sign out button not found")
                return False
        except Exception as e:
            self.log.error(f"Error clicking sign out: {str(e)}")
            return False

    def perform_logout(self):
        """Complete logout flow"""
        try:
            self.log.info("Starting logout process")

            # Click user profile menu (TO button)
            if not self.click_user_profile_menu():
                return False

            # Look for sign out button and click it (with scroll down)
            if not self.click_sign_out():
                return False

            self.log.info("Logout process completed")
            return True

        except Exception as e:
            self.log.error(f"Error in logout process: {str(e)}")
            return False

    # VERIFICATION METHODS
    def verify_login_success(self):
        """Verify successful login by checking for welcome message or dashboard"""
        try:
            # Wait a bit for page to load after login
            self.util.sleep(3)

            # Check for multiple success indicators
            success_indicators = [
                self._welcome_message,
                self._dashboard_indicator,
                "//h1[contains(text(), 'Welcome')]",
                "//*[contains(text(), 'Dashboard')]",
                "//*[contains(text(), 'Total Files')]",
                "//div[contains(@class, 'dashboard')]"
            ]

            for indicator in success_indicators:
                if self.isElementPresent(indicator, "xpath"):
                    element = self.getElement(indicator, "xpath")
                    if element and element.is_displayed():
                        self.log.info(f"Login success verified with: {indicator}")
                        return True

            # Also check URL for dashboard or user area
            current_url = self.driver.current_url.lower()
            url_indicators = ["dashboard", "app", "user", "home"]

            for indicator in url_indicators:
                if indicator in current_url:
                    self.log.info(f"Login success verified by URL containing: {indicator}")
                    return True

            self.log.info("Login success not verified")
            return False

        except Exception as e:
            self.log.error(f"Error verifying login success: {str(e)}")
            return False

    def verify_welcome_back_message(self):
        """Verify 'Welcome back' message is displayed"""
        try:
            welcome_back_selectors = [
                self._welcome_back_message,
                "//h1[contains(text(), 'Welcome back')]",
                "//h2[contains(text(), 'Welcome back')]",
                "//*[contains(text(), 'Welcome back')]"
            ]

            for selector in welcome_back_selectors:
                if self.isElementPresent(selector, "xpath"):
                    element = self.getElement(selector, "xpath")
                    if element and element.is_displayed():
                        self.log.info("'Welcome back' message verified")
                        return True

            self.log.info("'Welcome back' message not found")
            return False

        except Exception as e:
            self.log.error(f"Error verifying welcome back message: {str(e)}")
            return False

    def verify_check_your_email_message(self):
        """Verify 'Check your email' message for password reset"""
        try:
            email_message_selectors = [
                self._check_your_email_message,
                "//h1[contains(text(), 'Check your email')]",
                "//h2[contains(text(), 'Check your email')]",
                "//*[contains(text(), 'Check your email')]",
                "//*[contains(text(), 'password reset link')]"
            ]

            for selector in email_message_selectors:
                if self.isElementPresent(selector, "xpath"):
                    element = self.getElement(selector, "xpath")
                    if element and element.is_displayed():
                        self.log.info("'Check your email' message verified")
                        return True

            self.log.info("'Check your email' message not found")
            return False

        except Exception as e:
            self.log.error(f"Error verifying check your email message: {str(e)}")
            return False

    def verify_logout_success(self):
        """Verify successful logout by checking for welcome back message"""
        try:
            self.util.sleep(2)  # Wait for redirect after logout

            # Check if back to login page
            if self.verify_welcome_back_message():
                return True

            # Check URL for login/auth indicators
            current_url = self.driver.current_url.lower()
            logout_indicators = ["login", "signin", "auth", "welcome"]

            for indicator in logout_indicators:
                if indicator in current_url:
                    self.log.info(f"Logout success verified by URL containing: {indicator}")
                    return True

            self.log.info(" Logout success not verified")
            return False

        except Exception as e:
            self.log.error(f"Error verifying logout success: {str(e)}")
            return False

    def verify_login_failed(self):
        """Verify login failed (error message or still on login page)"""
        try:
            # Check for error messages
            if self.isElementPresent(self._error_message, "xpath"):
                self.log.info(" Login failure verified - error message present")
                return True

            # Check if still on login page
            if self.verify_welcome_back_message():
                self.log.info("Login failure verified - still on login page")
                return True

            # Check URL still contains login indicators
            current_url = self.driver.current_url.lower()
            if any(indicator in current_url for indicator in ["login", "signin", "auth"]):
                self.log.info("Login failure verified - still on auth page")
                return True

            return False

        except Exception as e:
            self.log.error(f"Error verifying login failure: {str(e)}")
            return False

    # NAVIGATION VERIFICATION
    def verify_back_to_signin_navigation(self):
        """Verify back to sign in navigation works"""
        try:
            if self.isElementPresent(self._back_to_signin_button, "xpath"):
                self.elementClick(self._back_to_signin_button, "xpath")
                self.util.sleep(2)

                # Verify we're back to login page
                return self.verify_welcome_back_message()

            return False

        except Exception as e:
            self.log.error(f"Error verifying back to signin navigation: {str(e)}")
            return False

    # UTILITY METHODS
    def get_current_page_title(self):
        """Get current page title"""
        try:
            return self.driver.title
        except Exception as e:
            self.log.error(f"Error getting page title: {str(e)}")
            return ""

    def get_current_url(self):
        """Get current URL"""
        try:
            return self.driver.current_url
        except Exception as e:
            self.log.error(f"Error getting current URL: {str(e)}")
            return ""

    def take_screenshot(self, filename=None):
        """Take screenshot for debugging"""
        try:
            if filename is None:
                filename = f"login_screenshot_{int(time.time())}.png"

            self.driver.save_screenshot(filename)
            self.log.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            self.log.error(f"Error taking screenshot: {str(e)}")
            return None

    def wait_for_element_and_click(self, locator, timeout=10):
        """Wait for element to be clickable and click it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            )
            element.click()
            return True
        except Exception as e:
            self.log.error(f"Error waiting for and clicking element: {str(e)}")
            return False

    def is_user_logged_in(self):
        """Check if user is currently logged in"""
        try:
            # Check for dashboard or user menu presence
            login_indicators = [
                self._user_profile_button,
                self._dashboard_indicator,
                "//div[contains(@class, 'dashboard')]",
                "//button[contains(@class, 'user')]"
            ]

            for indicator in login_indicators:
                if self.isElementPresent(indicator, "xpath"):
                    return True

            # Check URL
            current_url = self.driver.current_url.lower()
            if any(indicator in current_url for indicator in ["dashboard", "app", "user"]):
                return True

            return False

        except Exception as e:
            self.log.error(f"Error checking login status: {str(e)}")
            return False

    # ALTERNATIVE VALIDATION METHODS
    def get_current_url_state(self):
        """Get current URL to check for navigation changes"""
        try:
            return self.driver.current_url
        except Exception as e:
            self.log.error(f"Error getting current URL: {str(e)}")
            return None

    def check_form_field_values(self):
        """Check if form fields retain their values after failed submission"""
        try:
            form_state = {}

            # Check email field value
            if self.isElementPresent(self._email_input, "xpath"):
                email_element = self.getElement(self._email_input, "xpath")
                form_state['email'] = email_element.get_attribute('value') if email_element else ""

            # Check password field value (if visible)
            if self.isElementPresent(self._password_input, "xpath"):
                password_element = self.getElement(self._password_input, "xpath")
                form_state['password'] = password_element.get_attribute('value') if password_element else ""

            self.log.info(f"Form state captured: {form_state}")
            return form_state
        except Exception as e:
            self.log.error(f"Error checking form field values: {str(e)}")
            return {}

    def is_submit_button_enabled(self):
        """Check if submit button is enabled/clickable"""
        try:
            if self.isElementPresent(self._login_submit_button, "xpath"):
                button = self.getElement(self._login_submit_button, "xpath")
                if button:
                    is_enabled = button.is_enabled()
                    is_displayed = button.is_displayed()
                    self.log.info(f"Submit button - Enabled: {is_enabled}, Displayed: {is_displayed}")
                    return is_enabled and is_displayed
            return False
        except Exception as e:
            self.log.error(f"Error checking submit button state: {str(e)}")
            return False

    def monitor_network_activity(self):
        """Monitor if network requests are made during form submission"""
        try:
            # Get browser logs to check for network activity
            logs = self.driver.get_log('performance')
            network_requests = []

            for log in logs:
                message = log.get('message', '')
                if 'Network.request' in message or 'Network.response' in message:
                    network_requests.append(log)

            self.log.info(f"Network activity detected: {len(network_requests)} requests")
            return len(network_requests) > 0
        except Exception as e:
            self.log.error(f"Error monitoring network activity: {str(e)}")
            return None

    def validate_form_behavior_on_invalid_data(self, initial_url, initial_form_state):
        """Comprehensive validation of form behavior with invalid data"""
        try:
            validation_results = {
                'url_unchanged': False,
                'form_data_persisted': False,
                'submit_button_functional': False,
                'no_navigation_occurred': False
            }

            # Check URL hasn't changed (no navigation)
            current_url = self.get_current_url_state()
            validation_results['url_unchanged'] = (current_url == initial_url)
            validation_results['no_navigation_occurred'] = validation_results['url_unchanged']

            # Check form data persistence
            current_form_state = self.check_form_field_values()
            if initial_form_state and current_form_state:
                # Check if email field retained its value
                email_persisted = (
                        initial_form_state.get('email', '') == current_form_state.get('email', '') and
                        current_form_state.get('email', '') != ''
                )
                validation_results['form_data_persisted'] = email_persisted

            # Check submit button state
            validation_results['submit_button_functional'] = self.is_submit_button_enabled()

            self.log.info(f"Form validation results: {validation_results}")
            return validation_results

        except Exception as e:
            self.log.error(f"Error validating form behavior: {str(e)}")
            return None