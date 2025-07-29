"""
Enhanced Login Page - Verbatimly signup and login page object
Based on the actual HTML structure from the application
With enhanced validation and email verification support
"""

import logging
from base.basepage import BasePage
from utilities.util import Util
import utilities.custom_logger as cl
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    """Enhanced page object for Verbatimly signup and login functionality"""

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.log = cl.customLogger(logging.DEBUG)
        self.util = Util()

    # EXACT LOCATORS FROM HTML INSPECTION
    # Navigation elements
    _back_to_home_button = "//button[contains(text(), 'Back to home')]"
    _verbatimly_logo = "//span[contains(text(), 'Verbatimly')]"

    # Form fields (using exact IDs from HTML)
    _first_name_field = "//input[@id='firstName']"
    _last_name_field = "//input[@id='lastName']"
    _email_field = "//input[@id='email']"
    _password_field = "//input[@id='password']"
    _confirm_password_field = "//input[@id='confirmPassword']"
    _terms_checkbox = "//input[@id='agreeToTerms']"
    _create_account_button = "//button[@type='submit' and contains(., 'Create account')]"

    # Alternative locators using name attributes as backup
    _first_name_field_alt = "//input[@name='firstName']"
    _last_name_field_alt = "//input[@name='lastName']"
    _email_field_alt = "//input[@name='email']"
    _password_field_alt = "//input[@name='password']"
    _confirm_password_field_alt = "//input[@name='confirmPassword']"
    _terms_checkbox_alt = "//input[@name='agreeToTerms']"

    # Password visibility toggles
    _password_toggle = "//input[@id='password']//following-sibling::button"
    _confirm_password_toggle = "//input[@id='confirmPassword']//following-sibling::button"

    # Social login
    _google_signup_button = "//button[contains(., 'Google')]"
    _signin_link = "//button[contains(text(), 'Sign in')]"

    # Success/Error indicators and validation messages
    _page_title_heading = "//h1[contains(text(), 'Create your account')]"
    _email_verification_heading = "//h1[contains(text(), 'Check your email')]"
    _check_your_email_message = "//*[contains(text(), 'Check your email')]"
    _error_message = "//div[contains(@class, 'error') or contains(@class, 'alert')]"

    # Validation message selectors
    _validation_error = "//div[contains(@class, 'error-message')]"
    _field_error = "//span[contains(@class, 'field-error')]"
    _form_error = "//div[contains(@class, 'form-error')]"

    # Navigation methods
    def navigate_to_signup_page(self):
        """Navigate to signup page from any page"""
        try:
            current_url = self.driver.current_url
            if "auth/signup" not in current_url:
                signup_url = "https://dev-verbatimly.onrender.com/auth/signup"
                self.driver.get(signup_url)
                self.util.sleep(2)

            # Verify we're on the signup page
            return self.isElementPresent(self._page_title_heading, "xpath") or \
                   self.isElementPresent(self._first_name_field, "xpath")
        except Exception as e:
            self.log.error(f"Error navigating to signup page: {str(e)}")
            return False

    def click_back_to_home(self):
        """Click back to home button"""
        try:
            self.elementClick(self._back_to_home_button, "xpath")
            self.util.sleep(2)
            return True
        except Exception as e:
            self.log.error(f"Error clicking back to home: {str(e)}")
            return False

    # Enhanced form interaction methods
    def enter_first_name(self, first_name):
        """Enter first name with enhanced error handling"""
        try:
            # Clear field first
            self.clear_field(self._first_name_field)

            if self.isElementPresent(self._first_name_field, "xpath"):
                self.sendKeys(first_name, self._first_name_field, "xpath")
            else:
                self.sendKeys(first_name, self._first_name_field_alt, "xpath")
            self.log.info(f"Entered first name: {first_name}")
            return True
        except Exception as e:
            self.log.error(f"Error entering first name: {str(e)}")
            return False

    def enter_last_name(self, last_name):
        """Enter last name with enhanced error handling"""
        try:
            # Clear field first
            self.clear_field(self._last_name_field)

            if self.isElementPresent(self._last_name_field, "xpath"):
                self.sendKeys(last_name, self._last_name_field, "xpath")
            else:
                self.sendKeys(last_name, self._last_name_field_alt, "xpath")
            self.log.info(f"Entered last name: {last_name}")
            return True
        except Exception as e:
            self.log.error(f"Error entering last name: {str(e)}")
            return False

    def enter_email(self, email):
        """Enter email address with enhanced error handling"""
        try:
            # Clear field first
            self.clear_field(self._email_field)

            if self.isElementPresent(self._email_field, "xpath"):
                self.sendKeys(email, self._email_field, "xpath")
            else:
                self.sendKeys(email, self._email_field_alt, "xpath")
            self.log.info(f"Entered email: {email}")
            return True
        except Exception as e:
            self.log.error(f"Error entering email: {str(e)}")
            return False

    def enter_password(self, password):
        """Enter password with enhanced error handling"""
        try:
            # Clear field first
            self.clear_field(self._password_field)

            if self.isElementPresent(self._password_field, "xpath"):
                self.sendKeys(password, self._password_field, "xpath")
            else:
                self.sendKeys(password, self._password_field_alt, "xpath")
            self.log.info("Entered password")
            return True
        except Exception as e:
            self.log.error(f"Error entering password: {str(e)}")
            return False

    def enter_confirm_password(self, password):
        """Enter confirm password with enhanced error handling"""
        try:
            # Clear field first
            self.clear_field(self._confirm_password_field)

            if self.isElementPresent(self._confirm_password_field, "xpath"):
                self.sendKeys(password, self._confirm_password_field, "xpath")
            else:
                self.sendKeys(password, self._confirm_password_field_alt, "xpath")
            self.log.info("Entered confirm password")
            return True
        except Exception as e:
            self.log.error(f"Error entering confirm password: {str(e)}")
            return False

    def accept_terms_and_conditions(self):
        """Click the terms and conditions checkbox with enhanced handling"""
        try:
            # Check if checkbox is already checked
            checkbox_element = None
            if self.isElementPresent(self._terms_checkbox, "xpath"):
                checkbox_element = self.getElement(self._terms_checkbox, "xpath")
            else:
                checkbox_element = self.getElement(self._terms_checkbox_alt, "xpath")

            if checkbox_element and not checkbox_element.is_selected():
                if self.isElementPresent(self._terms_checkbox, "xpath"):
                    self.elementClick(self._terms_checkbox, "xpath")
                else:
                    self.elementClick(self._terms_checkbox_alt, "xpath")
                self.log.info("Accepted terms and conditions")
            else:
                self.log.info("Terms checkbox already checked")

            return True
        except Exception as e:
            self.log.error(f"Error accepting terms: {str(e)}")
            return False

    def click_create_account(self):
        """Click the Create Account button with enhanced handling"""
        try:
            # Wait for button to be clickable
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self._create_account_button))
            )

            self.elementClick(self._create_account_button, "xpath")
            self.log.info("Clicked Create Account button")
            self.util.sleep(3)  # Wait for form submission
            return True
        except Exception as e:
            self.log.error(f"Error clicking create account: {str(e)}")
            return False

    def click_google_signup(self):
        """Click Google signup button"""
        try:
            self.elementClick(self._google_signup_button, "xpath")
            self.log.info("Clicked Google signup")
            return True
        except Exception as e:
            self.log.error(f"Error clicking Google signup: {str(e)}")
            return False

    # Enhanced complete registration flow
    def complete_registration(self, first_name, last_name, email, password, confirm_password=None):
        """Complete the entire registration process with enhanced validation"""
        try:
            if confirm_password is None:
                confirm_password = password

            self.log.info(f"Starting registration for: {email}")

            # Navigate to signup page if not already there
            if not self.navigate_to_signup_page():
                self.log.error("Failed to navigate to signup page")
                return False

            # Wait for page to load completely
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self._first_name_field))
            )

            # Fill out the form step by step
            steps = [
                ("First Name", lambda: self.enter_first_name(first_name)),
                ("Last Name", lambda: self.enter_last_name(last_name)),
                ("Email", lambda: self.enter_email(email)),
                ("Password", lambda: self.enter_password(password)),
                ("Confirm Password", lambda: self.enter_confirm_password(confirm_password)),
                ("Terms", lambda: self.accept_terms_and_conditions()),
                ("Submit", lambda: self.click_create_account())
            ]

            for step_name, step_function in steps:
                if not step_function():
                    self.log.error(f"Failed at step: {step_name}")
                    return False
                time.sleep(0.5)  # Small delay between steps

            self.log.info("Registration form completed successfully")
            return True

        except Exception as e:
            self.log.error(f"Error completing registration: {str(e)}")
            return False

    # Enhanced verification methods
    def verify_signup_page_loaded(self):
        """Verify that the signup page has loaded correctly"""
        try:
            # Multiple indicators of successful page load
            indicators = [
                self.isElementPresent(self._page_title_heading, "xpath"),
                self.isElementPresent(self._first_name_field, "xpath") or self.isElementPresent(self._first_name_field_alt, "xpath"),
                self.isElementPresent(self._create_account_button, "xpath"),
                "signup" in self.driver.current_url.lower()
            ]

            if any(indicators):
                self.log.info("Signup page loaded successfully")
                return True
            else:
                self.log.error("Signup page not loaded properly")
                return False
        except Exception as e:
            self.log.error(f"Error verifying signup page: {str(e)}")
            return False

    def verify_check_your_email_message(self):
        """Enhanced verification for 'Check your email' message"""
        try:
            # Multiple selectors to find the success message
            success_selectors = [
                self._email_verification_heading,
                self._check_your_email_message,
                "//h1[contains(text(), 'Check your email')]",
                "//h2[contains(text(), 'Check your email')]",
                "//div[contains(text(), 'Check your email')]",
                "//span[contains(text(), 'Check your email')]",
                "//*[contains(text(), 'verify your email')]",
                "//*[contains(text(), 'verification email')]"
            ]

            for selector in success_selectors:
                if self.isElementPresent(selector, "xpath"):
                    element = self.getElement(selector, "xpath")
                    if element and element.is_displayed():
                        self.log.info("✅ 'Check your email' message found - Registration successful")
                        return True

            # Also check URL for verification indicators
            current_url = self.driver.current_url.lower()
            url_indicators = ["verify", "email", "confirmation", "check"]

            if any(indicator in current_url for indicator in url_indicators):
                self.log.info("✅ Email verification URL detected - Registration successful")
                return True

            self.log.info("❌ 'Check your email' message not found")
            return False

        except Exception as e:
            self.log.error(f"Error verifying email message: {str(e)}")
            return False

    def verify_registration_successful(self):
        """Comprehensive verification that registration was successful"""
        try:
            # Primary indicator: "Check your email" message
            if self.verify_check_your_email_message():
                return True

            # Secondary: Check for email verification page elements
            verification_indicators = [
                "//div[contains(@class, 'verification')]",
                "//div[contains(@class, 'success')]",
                "//img[contains(@alt, 'email')]",
                "//p[contains(text(), 'sent')]",
                "//p[contains(text(), 'inbox')]"
            ]

            for indicator in verification_indicators:
                if self.isElementPresent(indicator, "xpath"):
                    self.log.info("Registration successful - verification page elements found")
                    return True

            return False

        except Exception as e:
            self.log.error(f"Error verifying registration success: {str(e)}")
            return False

    def verify_registration_failed(self):
        """Verify registration failed (still on signup page or error shown)"""
        try:
            # Check if still on signup page
            still_on_signup = (
                self.isElementPresent(self._create_account_button, "xpath") or
                "signup" in self.driver.current_url.lower()
            )

            # Check for error messages
            error_present = (
                self.isElementPresent(self._error_message, "xpath") or
                self.isElementPresent(self._validation_error, "xpath") or
                self.isElementPresent(self._field_error, "xpath")
            )

            # Check for validation messages on fields
            validation_present = self.check_for_validation_messages()

            if still_on_signup or error_present or validation_present:
                self.log.info("Registration failed as expected")
                return True

            return False

        except Exception as e:
            self.log.error(f"Error verifying registration failure: {str(e)}")
            return False

    def check_for_validation_messages(self):
        """Check for any validation messages on the form"""
        try:
            fields_to_check = [
                self._first_name_field,
                self._last_name_field,
                self._email_field,
                self._password_field,
                self._confirm_password_field,
                self._terms_checkbox
            ]

            for field in fields_to_check:
                try:
                    element = self.getElement(field, "xpath")
                    if element:
                        validation_message = element.get_attribute("validationMessage")
                        if validation_message:
                            self.log.info(f"Validation message found: {validation_message}")
                            return True
                except:
                    continue

            return False

        except Exception as e:
            self.log.error(f"Error checking validation messages: {str(e)}")
            return False

    # Enhanced security testing methods
    def inject_sql_payload(self, field_name, payload):
        """Inject SQL payload into specified field with enhanced handling"""
        try:
            field_map = {
                "first_name": self._first_name_field,
                "last_name": self._last_name_field,
                "email": self._email_field
            }

            if field_name not in field_map:
                self.log.error(f"Invalid field name: {field_name}")
                return False

            # Clear field first
            self.clear_field(field_map[field_name])

            # Inject payload
            self.sendKeys(payload, field_map[field_name], "xpath")
            self.log.info(f"Injected SQL payload into {field_name}: {payload[:50]}...")
            return True

        except Exception as e:
            self.log.error(f"Error injecting SQL payload: {str(e)}")
            return False

    def inject_xss_payload(self, field_name, payload):
        """Inject XSS payload into specified field with enhanced handling"""
        try:
            field_map = {
                "first_name": self._first_name_field,
                "last_name": self._last_name_field,
                "email": self._email_field
            }

            if field_name not in field_map:
                self.log.error(f"Invalid field name: {field_name}")
                return False

            # Clear field first
            self.clear_field(field_map[field_name])

            # Inject payload
            self.sendKeys(payload, field_map[field_name], "xpath")
            self.log.info(f"Injected XSS payload into {field_name}: {payload[:50]}...")
            return True

        except Exception as e:
            self.log.error(f"Error injecting XSS payload: {str(e)}")
            return False

    # Enhanced utility methods
    def clear_field(self, field_locator):
        """Clear a specific field safely"""
        try:
            element = self.getElement(field_locator, "xpath")
            if element:
                element.clear()
                time.sleep(0.2)  # Small delay after clearing
            return True
        except Exception as e:
            self.log.error(f"Error clearing field: {str(e)}")
            return False

    def clear_all_fields(self):
        """Clear all form fields with enhanced error handling"""
        try:
            fields = [
                self._first_name_field,
                self._last_name_field,
                self._email_field,
                self._password_field,
                self._confirm_password_field
            ]

            for field in fields:
                self.clear_field(field)

            # Also uncheck terms checkbox if checked
            try:
                checkbox = self.getElement(self._terms_checkbox, "xpath")
                if checkbox and checkbox.is_selected():
                    self.elementClick(self._terms_checkbox, "xpath")
            except:
                pass

            self.log.info("Cleared all form fields")
            return True
        except Exception as e:
            self.log.error(f"Error clearing fields: {str(e)}")
            return False

    def get_field_validation_message(self, field_locator):
        """Get validation message for a specific field"""
        try:
            # Try HTML5 validation message first
            element = self.getElement(field_locator, "xpath")
            if element:
                validation_message = element.get_attribute("validationMessage")
                if validation_message:
                    return validation_message

            # Try to find custom error messages near the field
            error_selectors = [
                f"{field_locator}//following-sibling::div[contains(@class, 'error')]",
                f"{field_locator}//following-sibling::span[contains(@class, 'error')]",
                f"{field_locator}//parent::div//following-sibling::div[contains(@class, 'error')]",
                f"{field_locator}//parent::label//following-sibling::div[contains(@class, 'error')]"
            ]

            for selector in error_selectors:
                try:
                    error_element = self.getElement(selector, "xpath")
                    if error_element and error_element.is_displayed():
                        return error_element.text.strip()
                except:
                    continue

            return None

        except Exception as e:
            self.log.error(f"Error getting field validation message: {str(e)}")
            return None

    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except Exception as e:
            self.log.error(f"Page load timeout: {str(e)}")
            return False

    def get_current_page_title(self):
        """Get current page title with enhanced error handling"""
        try:
            return self.getTitle()
        except Exception as e:
            self.log.error(f"Error getting page title: {str(e)}")
            return ""

    def get_current_url(self):
        """Get current URL safely"""
        try:
            return self.driver.current_url
        except Exception as e:
            self.log.error(f"Error getting current URL: {str(e)}")
            return ""

    def take_screenshot(self, filename=None):
        """Take screenshot for debugging"""
        try:
            if filename is None:
                filename = f"screenshot_{int(time.time())}.png"

            self.driver.save_screenshot(filename)
            self.log.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            self.log.error(f"Error taking screenshot: {str(e)}")
            return None

    def scroll_to_element(self, locator, locator_type="xpath"):
        """Scroll to element to ensure it's visible"""
        try:
            element = self.getElement(locator, locator_type)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            self.log.error(f"Error scrolling to element: {str(e)}")
            return False

    def refresh_page(self):
        """Refresh the current page"""
        try:
            self.driver.refresh()
            self.util.sleep(3)
            return True
        except Exception as e:
            self.log.error(f"Error refreshing page: {str(e)}")
            return False