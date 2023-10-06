import utilities.custom_logger as cl

import logging
from base.basepage import BasePage
from utilities.util import Util
from selenium.common.exceptions import*


class LoginPage(BasePage):
    """
            Initialize LoginPage class with driver instance and NavigationPage instance.

            Args:
            - driver: WebDriver instance.
            """


    log2 = Util()
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    # Locators
    _start_link = "//a[contains(text(), 'Started')]"
    _email_field = "//input[contains(@id, 'email')]"
    _password_field = "//div//input[contains(@id, 'password')]"
    _user_name_field = "//div//input[contains(@id, 'username')]"
    _cookies = "//div//button[contains(text(), 'Accept')]"
    _create_account = "//button[contains(text(), 'Create')]"
    # _search_domain = "//form//input[contains(@id, 'search')]"
    _choose_domain_later = "(//button//span[contains(text(), 'domain')])[2]"  # wait for some 3sec to load
    _start_with_free = "(//div//button[contains(text(), 'Free')])[1]"
    _sell_online = "(//span//input[contains(@id, 'select-card-checkbox-1')])[1]"
    _other = "(//div//span[contains(text(), 'Other')])[1]"
    _continue = "(//div//button[contains(text(), 'Continue')])[1]"  # same with second continue
    _store_name = "(//input[contains(@id, 'siteTitle')])[1]"
    _tagline = "(//input[contains(@id, 'tagline')])[1]"
    _continue2 = "(//div//button[contains(text(), 'Continue')])[1]"  # same with second continue
    _skip_for_now = "(//div//button[contains(text(), 'Skip')])[1]"
    _my_store = "(//div//span[contains(text(), 'Site')])[1]"  # This for login validation 1
    _icon = "(//span//img[contains(@alt, 'My Profile')])[1]"  # second login verification
    _log_out = "(//button//span[contains(text(), 'out')])[1]"
    _word_press_logo = "(//h1//a[contains(text(), 'WordPress')])[1]"  # one verification for succesful logout or the presence of mainlogin

    #new way to navigate.
    _continue_with_google = "//span[contains(text(),'Google')]"
    _email_or_phone_field = "//div//input[contains(@id,'identifierId')]"
    _create_account_from_gmail = "//div//span[contains(text(),'Create')]"
    _next_button = "//div//span[contains(text(),'Next')]"
    # Couldn't find your Google Account....if u use invalid email and click next...but if you use create account
    #instead it will ask for your vorname and nachnamen
    _first_name_field = "//input[contains(@id,'firstName')]"
    _last_name_field = "//input[contains(@id,'lastName')]"
    _click_weiter = "//span[contains(text(),'Weiter')]"
    _tag = "//*[@id='day']"
    _month = "//*[@id='month']"
    _year = "//*[@id='year']"
    _gender = "//*[@id='gender']"
    _click_weiter_again = "//span[contains(text(),'Weiter')]"

    #after filling the date of birth field and clicking on the second weiter it will suggest 3 gmail for you t
    #to choose from
    _choose_suggested_email = "//div[contains(@id,'selectionc0')]" # 1st one....kelvinobutubaga@gmail.com...pass:##ACGTY678cde
    _choose_suggested_email2 = "//div[contains(@id,'selectionc1')]"
    _choose_suggested_email3 = "//div[contains(@id,'selectionc2')]" # this 3rd option is to create urself
    _next_password_field = "(//div//input[contains(@name,'Passwd')])[1]"
    _confirm_password_field = "(//div//input[contains(@name,'PasswdAgain')])[1]"
    _click_weiter_again_again =_click_weiter
    # Next is password field to provide ur phone no. it shows that this is outside the wordpress rather
    #more of google registration. so I stop here.

    #Invalid Alerts Locators:
    _invalid_email_alert = "//div//span[contains(text(), 'working')]"
    _invalid_username_alert = "//div//span[contains(text(), 'choice')]"
    _invalid_password_alert = "//div//span[contains(text(), 'forget')]"


    def clickStartFree(self):
        self.elementClick(self._start_link, locatorType="xpath")

    def emailField(self):
        self.elementClick(self._email_field, locatorType="xpath")

    def enterEmail(self, email):
        self.sendKeys(email, self._email_field, locatorType="xpath")

    def usernameField(self):
        self.elementClick(self._user_name_field, locatorType="xpath")

    def enterUserName(self, username):
        self.sendKeys(username, self._user_name_field, locatorType="xpath")
    def clickCookies(self):
        self.elementClick(self._cookies, locatorType="xpath")
    def passwordField(self):
        self.elementClick(self._password_field, locatorType="xpath")
    def enterPassword(self, password):
        self.sendKeys(password, self._password_field, locatorType="xpath")

    def createAccount(self):
        self.elementClick(self._create_account, locatorType="xpath")
    def chooseDomainname(self):
        self.elementClick(self._choose_domain_later, locatorType="xpath")
    def startFree(self):
        self.elementClick(self._start_with_free, locatorType="xpath")
    def sellOnline(self):
        self.elementClick(self._sell_online, locatorType="xpath")
    def other(self):
        self.elementClick(self._other, locatorType="xpath")

    def clickContinue(self):
        self.elementClick(self._continue, locatorType="xpath")
    # def storeName(self):
    #     self.elementClick(self._store_name, locatorType="xpath")
    # def tagLine(self):
    #     self.elementClick(self._tagline, locatorType="xpath")
    def skipForNow(self):
        self.elementClick(self._skip_for_now, locatorType="xpath")  # wait for page to load like 3secs

    def createAccountPage(self, email="", password="", username=""):
        """
                Perform login action.

                Args:
                - email (str): Email address for login.
                - password (str): Password for login.
                """
        self.clickStartFree()

        self.emailField()
        self.log2.sleep(3)
        self.enterEmail(email)
        self.log2.sleep(3)
        self.usernameField()
        self.log2.sleep(3)
        self.enterUserName(username)
        self.clickCookies()
        self.log2.sleep(3)
        self.passwordField()
        self.log2.sleep(3)
        self.enterPassword(password)
        self.log2.sleep(3)
        self.createAccount()
        self.log2.sleep(3)

        self.chooseDomainname()
        self.startFree()
        self.log2.sleep(3)
        self.sellOnline()
        self.log2.sleep(3)
        self.other()
        self.log2.sleep(3)
        self.clickContinue()
        self.log2.sleep(3)
        self.clickContinue()
        self.log2.sleep(3)

        self.skipForNow()

    def createAccountPage2(self, email="", password="", username=""):
        """
                Perform login action.

                Args:
                - email (str): Email address for login.
                - password (str): Password for login.
                """
        self.clickStartFree()

        self.emailField()
        self.log2.sleep(3)
        self.enterEmail(email)
        self.log2.sleep(3)
        self.usernameField()
        self.log2.sleep(3)
        self.enterUserName(username)
        self.clickCookies()
        self.log2.sleep(3)
        self.passwordField()
        self.log2.sleep(3)
        self.enterPassword(password)
        self.log2.sleep(3)
        self.createAccount()
    def verifyAccountSuccessful(self):
        """
                Verify if login successful.

                Returns:
                - bool: True if login was successful, False otherwise.
                """
        result_first = self.waitForElement(self._my_store,
                                           locatorType="xpath")
        result = self.isElementPresent(locator=self._my_store,
                                       locatorType="xpath")
        return result
    def verifyAccountSuccessful2(self):


        result_first = self.waitForElement(self._icon,
                                           locatorType="xpath")
        result = self.isElementPresent(locator=self._icon,
                                       locatorType="xpath")
        return result

    def logout(self):
        logoutLinkElement = self.waitForElement(locator=self._icon,timeout=10,
                          locatorType="xpath", pollFrequency=1)
        self.elementClick(element=logoutLinkElement)
        self.elementClick(locator=self._log_out,
                          locatorType="xpath")
    def verifyLogoutSuccessful(self):

        """
                Verify if logout was successful.

                Returns:
                - bool: True if logout was successful, False otherwise.
                """
        result_first = self.waitForElement(self._word_press_logo,
                                           locatorType="xpath")
        actual_text=result_first.text
        result = self.log2.verifyTextMatch(actualText=actual_text, expectedText="WordPress.com")
        return result
    #
    def clearFields(self):
        emailField = self.getElement(locator=self._email_field)
        emailField.clear()
        passwordField = self.getElement(locator=self._password_field)
        passwordField.clear()

    def verifyinvalidAccountEmptyEmailSuccessful(self):
        """
                           Verify if invalid login with empty fields is successful.

                           Returns:
                           - bool: True if warning messages are displayed, False otherwise.
                           """
        result_email1 = self.waitForElement(self._invalid_email_alert,
                                              locatorType="xpath")
        result_email = self.isElementPresent(element=result_email1)
        if result_email:
            email_message = result_email1.text
            element_email = self.log2.verifyTextMatch(actualText=email_message,
                                                         expectedText="Enter a working email address, so you can receive our messages.")  # This returns boolean will be used in the
            # test class for assertion. Don't assert anything in the page object.
            print("Actual text" + email_message)
            return element_email
        else:
            print("NO SUCH ELEMENT FOUND" )
    def verifyinvalidAccountEmptyUsernameSuccessful(self):
        """
            Verify if invalid username with empty fields is successful.

             Returns:
             - bool: True if warning messages are displayed, False otherwise.
                                   """
        result_username1 = self.waitForElement(self._invalid_username_alert,
                                           locatorType="xpath")
        result_username = self.isElementPresent(element=result_username1)
        if result_username:
            username_message = result_username1.text
            element_username = self.log2.verifyTextMatch(actualText=username_message,
                                                  expectedText="Enter a username of your choice.")  # This returns boolean will be used in the
        # test class for assertion. Don't assert anything in the page object.
            print("Actual text" + username_message)
            return element_username
        else:
            print("NO SUCH ELEMENT FOUND" )

    def verifyinvalidAccountEmptyPasswordSuccessful(self):
        """
                    Verify if invalid password with empty fields is successful.

                     Returns:
                     - bool: True if warning messages are displayed, False otherwise.
                                           """
        result_password1 = self.waitForElement(self._invalid_password_alert,
                                               locatorType="xpath")
        result_password = self.isElementPresent(element=result_password1)
        if result_password:
            password_message = result_password1.text
            element_password = self.log2.verifyTextMatch(actualText=password_message,
                                                         expectedText="Don't forget to enter a password.")  # This returns boolean will be used in the
            # test class for assertion. Don't assert anything in the page object.
            print("Actual text" + password_message)
            return element_password
        else:
            print("NO SUCH ELEMENT FOUND")

    def verifyinvalidAccountNullEmailSuccessful(self):
        """
                           Verify if invalid login with empty fields is successful.

                           Returns:
                           - bool: True if warning messages are displayed, False otherwise.
                           """
        result_email1 = self.waitForElement(self._invalid_email_alert,
                                            locatorType="xpath")
        result_email = self.isElementPresent(element=result_email1)
        if result_email:
            email_message = result_email1.text
            element_email = self.log2.verifyTextMatch(actualText=email_message,
                                                      expectedText="Enter a working email address, so you can receive our messages.")  # This returns boolean will be used in the
            # test class for assertion. Don't assert anything in the page object.
            print("Actual text" + email_message)
            return element_email
        else:
            print("NO SUCH ELEMENT FOUND")

    def verifyinvalidAccountNullUsernameSuccessful(self):

        """
            Verify if invalid username with empty fields is successful.

             Returns:
             - bool: True if warning messages are displayed, False otherwise.
                                   """
        result_username1 = self.waitForElement(self._invalid_username_alert,
                                               locatorType="xpath")
        result_username = self.isElementPresent(element=result_username1)
        if result_username:
            username_message = result_username1.text
            element_username = self.log2.verifyTextMatch(actualText=username_message,
                                                         expectedText="Enter a username of your choice.")  # This returns boolean will be used in the
            # test class for assertion. Don't assert anything in the page object.
            print("Actual text" + username_message)
            return element_username
        else:
            print("NO SUCH ELEMENT FOUND")

    def verifyinvalidAccountNullPasswordSuccessful(self):
        """
                    Verify if invalid password with empty fields is successful.

                     Returns:
                     - bool: True if warning messages are displayed, False otherwise.
                                           """
        result_password1 = self.waitForElement(self._invalid_password_alert,
                                               locatorType="xpath")
        result_password = self.isElementPresent(element=result_password1)
        if result_password:
            password_message = result_password1.text
            element_password = self.log2.verifyTextMatch(actualText=password_message,
                                                         expectedText="Don't forget to enter a password.")  # This returns boolean will be used in the
            # test class for assertion. Don't assert anything in the page object.
            print("Actual text" + password_message)
            return element_password
        else:
            print("NO SUCH ELEMENT FOUND")

    #     continue_login = self.waitForElement(locator=self._continue_IfLogin,
    #                                          locatorType="xpath", pollFrequency=1)
    #     self.elementClick(element=continue_login)
    #     #self.log2.sleep(10)

    #     #self.clickLogin()
