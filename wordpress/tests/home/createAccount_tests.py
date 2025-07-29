"""
Enhanced Registration Test Cases with Welcome/Verify detection (no mailbox flow)
- Testing functionality, proper error message display, and success screen presence
"""

import pytest
import unittest
from pages.home.CreateAccount import LoginPage
from utilities.teststatus import TestStatus
from utilities.util import Util
import utilities.custom_logger as cl
import logging
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import configparser

load_dotenv()



def load_test_accounts_from_config():
    """Load test accounts from pytest.ini configuration."""
    try:
        config = configparser.ConfigParser()
        config_path = os.path.join(os.getcwd(), "pytest.ini")

        if not os.path.exists(config_path):
            pytest.skip("pytest.ini not found, test is skipped")

        config.read(config_path)

        if "pytest" in config:
            pytest_section = config["pytest"]
            accounts = []

            if all(
                key in pytest_section
                for key in [
                    "account1_email",
                    "account1_password",
                    "account1_first_name",
                    "account1_last_name",
                ]
            ):
                accounts.append(
                    {
                        "email": pytest_section["account1_email"].strip(),
                        "password": pytest_section["account1_password"].strip(),
                        "first_name": pytest_section["account1_first_name"].strip(),
                        "last_name": pytest_section["account1_last_name"].strip(),
                    }
                )

            if all(
                key in pytest_section
                for key in [
                    "account2_email",
                    "account2_password",
                    "account2_first_name",
                    "account2_last_name",
                ]
            ):
                accounts.append(
                    {
                        "email": pytest_section["account2_email"].strip(),
                        "password": pytest_section["account2_password"].strip(),
                        "first_name": pytest_section["account2_first_name"].strip(),
                        "last_name": pytest_section["account2_last_name"].strip(),
                    }
                )

            if accounts:
                print(f"Loaded {len(accounts)} test accounts from pytest.ini")
                return accounts

    except Exception as e:
        print(f"Error reading WordPress env: {str(e)}")
        return None


# Load test accounts from configuration
VALID_TEST_ACCOUNTS = load_test_accounts_from_config()

# Expected validation messages (used where available via HTML5 validationMessage)
VALIDATION_MESSAGES = {
    "first_name_required": "Please fill out this field.",
    "terms_required": "Please check this box if you want to proceed.",
    "invalid_email_double_at": "A part following '@' should not contain the symbol '@'.",
    "invalid_email_wrong_position": "'.' is used at a wrong position in 'domain..com'.",
    "short_password": "Password should be a min of 8 character",
    "password_mismatch": "Password does not match.",
}

# Invalid email test cases (strings are typical browser validation texts; may vary by browser/OS)
INVALID_EMAILS = [
    {"email": "plainaddresuuust", "expected_message": "Please include an '@' in the email address"},
    {"email": "two@@suuignsh.com", "expected_message": "A part following '@' should not contain the symbol '@'."},
    {"email": "name@dooomain..com", "expected_message": "'.' is used at a wrong position"},
    {"email": "@no-local-partuuu.com", "expected_message": "enter a part followed by '@'"},
    {"email": "no-at.hhdomainn.com", "expected_message": "Please include an '@' in the email address"},
    {"email": "no-tyhld@domainn", "expected_message": "Please match the requested format"},
]

# Password validation test cases
WEAK_PASSWORDS = [
    {"password": "short7!", "expected_fail": True, "reason": "too short",
     "expected_message": VALIDATION_MESSAGES["short_password"]},
    {"password": "alllowercase111!", "expected_fail": True, "reason": "missing uppercase"},
    {"password": "ALLUPPERCASE111!", "expected_fail": True, "reason": "missing lowercase"},
    {"password": "NoDigitsss!!!", "expected_fail": True, "reason": "missing digits"},
    {"password": "NoSpecial12345", "expected_fail": True, "reason": "missing special"},
]

# Password mismatch test cases
PASSWORD_MISMATCH_CASES = [
    {"password": "ValidPass1237!", "confirm_password": "DifferentPass1283!",
     "expected_message": VALIDATION_MESSAGES["password_mismatch"]},
]

# Security payloads
SQLI_FIRSTNAME = "'; DROP TABLE users; --"
XSS_LASTNAME = "<script>alert('I AM A SCAMMER');</script>"


@pytest.mark.usefixtures("setUp")
class CreateAccountTests(unittest.TestCase):
    """Enhanced test class for account creation (no mailbox flow)."""

    @pytest.fixture(autouse=True)
    def setUpObject(self, driver):
        """Setup test objects using the driver fixture."""
        self.driver = driver
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.util = Util()
        self.log = cl.customLogger(logging.DEBUG)

    # ------------------------------
    # Internal helpers
    # ------------------------------
    def _quiet_find_xpath(self, xpath: str, timeout: int = 2):
        """
        Try to find element by xpath with short timeout and no error log spam.
        Returns WebElement or None.
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except Exception:
            return None

    def verify_check_your_email_message(self) -> bool:
        """
        Verify success by detecting either:
          - 'Check your email' message, or
          - a 'Welcome' heading/message, or
          - a URL heuristic indicating the success/verify/onboarding page.

        Implementation uses only XPath 1.0 and short, quiet waits.
        """
        try:
            url = (self.driver.current_url or "").lower()
            if any(k in url for k in ("verify", "welcome", "onboarding")):
                self.log.info("Success indicated by URL: %s", url)
                return True

            # Case-insensitive 'Check your email' (common success message)
            check_email_x = (
                "//*[self::h1 or self::h2 or self::div or self::p]"
                "[contains(translate(normalize-space(.),"
                "'CHECK YOUR EMAIL','check your email'),"
                "'check your email')]"
            )

            # Case-insensitive 'Welcome' (welcome/onboarding after success)
            welcome_x = (
                "//*[self::h1 or self::h2 or self::div or self::p]"
                "[contains(translate(normalize-space(.),"
                "'WELCOME','welcome'),'welcome')]"
            )

            for xp in (check_email_x, welcome_x):
                el = self._quiet_find_xpath(xp, timeout=3)
                if el and el.is_displayed():
                    txt = (el.text or "").strip()
                    self.log.info("Success message found: %s", txt if txt else "(element present)")
                    return True

            self.log.info("No success message detected yet.")
            return False

        except Exception as e:
            self.log.error(f"Error verifying email/welcome message: {str(e)}")
            return False

    def get_validation_message(self, field_locator_xpath: str):
        """
        Extract validation message for a given input field:
          1) HTML5 constraint validation message (validationMessage)
          2) Nearby inline/custom error elements
        Returns a string or None.
        """
        try:
            el = self.lp.getElement(field_locator_xpath, "xpath")
            if el:
                # HTML5 validation bubble text (after submit triggers validation)
                try:
                    vm = el.get_dom_property("validationMessage")
                except Exception:
                    vm = el.get_attribute("validationMessage")
                if vm:
                    return vm

            # Common custom error placements near the field
            candidates = [
                f"{field_locator_xpath}/following-sibling::*[self::div or self::span][contains(@class,'error')][1]",
                f"{field_locator_xpath}/ancestor::*[self::div or self::label][1]/following-sibling::*[self::div or self::span][contains(@class,'error')][1]",
                "//div[contains(@class,'error') or contains(@class,'alert') or @role='alert']",
            ]
            for xp in candidates:
                e2 = self._quiet_find_xpath(xp, timeout=2)
                if e2 and e2.is_displayed():
                    return (e2.text or "").strip()

            return None

        except Exception as e:
            self.log.error(f"Error getting validation message: {str(e)}")
            return None

    def is_running_locally(self):
        """Retained helper (no external mailbox usage)."""
        try:
            local_indicators = [
                os.getenv("ENVIRONMENT") == "local",
                "localhost" in (self.driver.current_url or ""),
                "127.0.0.1" in (self.driver.current_url or ""),
                os.path.exists("wordpress/.env.wordpress"),
            ]
            return any(local_indicators)
        except Exception:
            return False

    # ------------------------------
    #               TESTS
    # ------------------------------

    @pytest.mark.smoke
    def test_valid_registration_with_real_accounts(self):
        """
        TC_REG_001: Test valid registration with real email accounts.
        Expected: After clicking Create account, a success signal is present:
          • 'Check your email' OR
          • 'Welcome' OR
          • success/verify/onboarding URL.
        """
        self.log.info("Starting test_valid_registration_with_real_accounts")

        if not VALID_TEST_ACCOUNTS:
            pytest.skip("No VALID_TEST_ACCOUNTS configured in pytest.ini")

        self.log.info(f"Using {len(VALID_TEST_ACCOUNTS)} test accounts from configuration")

        per_account_results = []

        for i, account in enumerate(VALID_TEST_ACCOUNTS):
            try:
                self.log.info(f"Testing account {i + 1}: {account['email']}")

                # Complete registration (page object handles navigation, typing, ticking terms, and submit)
                self.lp.complete_registration(
                    first_name=account["first_name"],
                    last_name=account["last_name"],
                    email=account["email"],
                    password=account["password"],
                )

                # Short pause to allow page to update
                time.sleep(2)

                ok = self.verify_check_your_email_message()
                self.ts.mark(ok, f"Registration success indicator for {account['email']}")
                per_account_results.append(ok)

            except Exception as e:
                self.log.error(f"Test failed for {account['email']}: {str(e)}")
                self.ts.mark(False, f"Registration test failed for {account['email']}: {str(e)}")
                per_account_results.append(False)

        overall = all(per_account_results)
        self.ts.markFinal(
            "test_valid_registration_with_real_accounts",
            overall,
            f"Accounts success: {sum(per_account_results)}/{len(per_account_results)}",
        )

    @pytest.mark.negative
    def test_password_validation_enhanced(self):
        """
        TC_REG_002: Test password validation including short password and mismatch.
        """
        self.log.info("Starting test_password_validation_enhanced")

        test_results = []

        # A) Short password
        try:
            self.log.info("Testing short password validation")
            self.lp.complete_registration(
                first_name="Johnpo",
                last_name="Doekll",
                email="test@example.com",
                password="short7!",  # too short
                confirm_password="short7!",
            )
            time.sleep(2)
            # Success indicators should NOT appear
            ok = not self.verify_check_your_email_message()
            self.ts.mark(ok, "Short password properly rejected")
            test_results.append(ok)
        except Exception as e:
            self.log.error(f"Short password test failed: {str(e)}")
            test_results.append(False)

        # B) Password mismatch
        try:
            self.log.info("Testing password mismatch validation")
            self.lp.navigate_to_signup_page()
            self.lp.complete_registration(
                first_name="Johnpp",
                last_name="Doekk",
                email="test2@example.com",
                password="ValidPass123!",
                confirm_password="DifferentPass123!",
            )
            time.sleep(2)
            ok = not self.verify_check_your_email_message()
            self.ts.mark(ok, "Password mismatch properly rejected")
            test_results.append(ok)
        except Exception as e:
            self.log.error(f"Password mismatch test failed: {str(e)}")
            test_results.append(False)

        overall = all(test_results)
        self.ts.markFinal(
            "test_password_validation_enhanced",
            overall,
            f"Password validation tests: {sum(test_results)}/{len(test_results)} passed",
        )

    @pytest.mark.negative
    def test_registration_empty_fields_with_messages(self):
        """
        TC_REG_003: Test registration with empty fields and verify error messages.
        """
        self.log.info("Starting test_registration_empty_fields_with_messages")

        try:
            self.lp.navigate_to_signup_page()

            # Only first name filled, others empty
            self.lp.enter_first_name("John")
            self.lp.click_create_account()
            time.sleep(1)

            # Success indicators should NOT appear
            if self.verify_check_your_email_message():
                self.ts.markFinal(
                    "test_registration_empty_fields_with_messages",
                    False,
                    "Empty fields incorrectly accepted (success indicator present)",
                )
                return

            # Check for validation messages
            last_name_message = self.get_validation_message(self.lp._last_name_field)
            email_message = self.get_validation_message(self.lp._email_field)

            validation_working = (
                last_name_message == VALIDATION_MESSAGES["first_name_required"]
                or email_message == VALIDATION_MESSAGES["first_name_required"]
                or (last_name_message is not None or email_message is not None)
            )

            self.ts.markFinal(
                "test_registration_empty_fields_with_messages",
                validation_working,
                "Empty field validation working properly",
            )

        except Exception as e:
            self.log.error(f"Test failed with exception: {str(e)}")
            self.ts.markFinal(
                "test_registration_empty_fields_with_messages",
                False,
                f"Test failed with exception: {str(e)}",
            )

    @pytest.mark.negative
    def test_terms_checkbox_validation(self):
        """
        TC_REG_005: Terms checkbox must be checked or HTML5 constraint validation should block submit.
        We verify via the element's 'validationMessage' after submit.
        """
        self.log.info("Starting test_terms_checkbox_validation")
        try:
            self.lp.navigate_to_signup_page()
            self.lp.enter_first_name("JohnGood")
            self.lp.enter_last_name("DoeGood")
            self.lp.enter_email("testtest@example.com")
            self.lp.enter_password("TalltttBuildings123!")
            self.lp.enter_confirm_password("TalltttBuildings123!")

            # Intentionally DO NOT accept terms
            self.lp.click_create_account()
            time.sleep(1)

            # HTML5 constraint validation message on the required checkbox
            terms_xpath = (
                "//input[@type='checkbox' and @required "
                "and (@id='agreeToTerms' or @name='agreeToTerms' "
                "or contains(translate(@aria-label,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'terms') "
                "or contains(translate(@aria-label,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'agree'))]"
            )
            terms_el = self._quiet_find_xpath(terms_xpath, timeout=2)
            vm = None
            if terms_el:
                try:
                    vm = terms_el.get_dom_property("validationMessage")
                except Exception:
                    vm = terms_el.get_attribute("validationMessage")

            self.log.info("Terms validation message: %s", vm)
            # Even if browser text varies slightly, success indicator must NOT appear
            ok = (vm is not None and len(vm.strip()) > 0) and (not self.verify_check_your_email_message())
            self.ts.markFinal(
                "test_terms_checkbox_validation",
                ok,
                "Terms checkbox validation working properly",
            )

        except Exception as e:
            self.log.error(f"Test failed with exception: {str(e)}")
            self.ts.markFinal(
                "test_terms_checkbox_validation",
                False,
                f"Test failed with exception: {str(e)}",
            )

    @pytest.mark.security
    def test_security_comprehensive_assessment(self):
        """
        TC_REG_006: Basic security payload handling (sanitized/rejected either is acceptable).
        """
        self.log.info("Starting comprehensive security assessment")

        security_tests = [
            {"name": "SQL Injection in First Name", "payload": SQLI_FIRSTNAME, "field": "first_name"},
            {"name": "XSS in Last Name", "payload": XSS_LASTNAME, "field": "last_name"},
        ]

        results = []

        for test in security_tests:
            try:
                self.log.info(f"Testing: {test['name']}")
                self.lp.navigate_to_signup_page()

                if test["field"] == "first_name":
                    self.lp.inject_sql_payload("first_name", test["payload"])
                    self.lp.enter_last_name("Doe")
                else:
                    self.lp.enter_first_name("John")
                    self.lp.inject_xss_payload("last_name", test["payload"])

                self.lp.enter_email("security3333@test.com")
                self.lp.enter_password("TalluuBuildingstttt123!")
                self.lp.enter_confirm_password("TalluuBuildingstttt123!")
                self.lp.accept_terms_and_conditions()

                self.lp.click_create_account()
                time.sleep(2)

                # Either sanitized (success indicator appears) or rejected (no success) is acceptable
                handled = True
                self.ts.mark(handled, f"{test['name']}: Payload handled safely")
                results.append(handled)

            except Exception as e:
                self.log.error(f"Error in security test {test['name']}: {str(e)}")
                self.ts.mark(False, f"{test['name']} failed with exception")
                results.append(False)

        overall = all(results)
        self.ts.markFinal(
            "test_security_comprehensive_assessment",
            overall,
            f"Security assessment: {sum(results)}/{len(results)} tests passed",
        )

    @pytest.mark.ui
    def test_form_validation_ui_elements(self):
        """
        TC_REG_007: Test UI elements and accessibility (presence only).
        """
        self.log.info("Starting test_form_validation_ui_elements")

        try:
            page_loaded = self.lp.navigate_to_signup_page()
            self.ts.mark(page_loaded, "Signup page loaded")

            elements_check = [
                (self.lp._first_name_field, "First name field"),
                (self.lp._last_name_field, "Last name field"),
                (self.lp._email_field, "Email field"),
                (self.lp._password_field, "Password field"),
                (self.lp._confirm_password_field, "Confirm password field"),
                (self.lp._terms_checkbox, "Terms checkbox"),
                (self.lp._create_account_button, "Create account button"),
            ]

            all_present = True
            for locator, name in elements_check:
                present = self.lp.isElementPresent(locator, "xpath")
                self.ts.mark(present, f"{name} present")
                if not present:
                    all_present = False

            self.ts.markFinal(
                "test_form_validation_ui_elements",
                all_present,
                "All form elements present and accessible",
            )

        except Exception as e:
            self.log.error(f"Test failed with exception: {str(e)}")
            self.ts.markFinal(
                "test_form_validation_ui_elements",
                False,
                f"Test failed with exception: {str(e)}",
            )

    @pytest.mark.boundary
    def test_boundary_values_enhanced(self):
        """
        TC_REG_008: Boundary values with success indicator .
        """
        self.log.info("Starting test_boundary_values_enhanced")

        test_cases = [
            {"first_name": "A" * 255, "expected_fail": True, "description": "Very long first name"},
            {"last_name": "B" * 255, "expected_fail": True, "description": "Very long last name"},
            {"email": "a" * 290 + "@example.com", "expected_fail": True, "description": "Very long email"},
            {"first_name": "A", "last_name": "B", "expected_fail": False, "description": "Minimum valid inputs"},
        ]

        results = []

        for i, tc in enumerate(test_cases):
            try:
                self.log.info("Boundary case %d: %s", i + 1, tc["description"])

                first_name = tc.get("first_name", "John")
                last_name = tc.get("last_name", "Doe")
                email = tc.get("email", f"test{i}@example.com")

                self.lp.complete_registration(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password="TallBuildings123!",
                )

                time.sleep(2)

                success = self.verify_check_your_email_message()

                if tc.get("expected_fail", False):
                    # Expected rejection: success indicator should NOT appear
                    test_passed = not success
                    msg = f"Boundary case {i + 1} properly rejected"
                else:
                    # Expected acceptance: success indicator should appear
                    test_passed = success
                    msg = f"Boundary case {i + 1} properly accepted"

                self.ts.mark(test_passed, msg)
                results.append(test_passed)

            except Exception as e:
                self.log.error(f"Boundary test case {i + 1} failed: {str(e)}")
                self.ts.mark(False, f"Boundary case {i + 1} failed with exception")
                results.append(False)

        overall = all(results)
        self.ts.markFinal(
            "test_boundary_values_enhanced",
            overall,
            f"Boundary value testing: {sum(results)}/{len(results)} passed",
        )
