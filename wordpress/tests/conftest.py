import pytest
from base.webdriverfactory import WebDriverFactory
from pages.home.login_page import LoginPage


# This fixture is for setting up and tearing down things that need to be done before and after each test method.
@pytest.fixture()
def setUp():
    print("Running method level setUp")
    yield  # This is where the test method will execute
    print("Running method level tearDown")


# This fixture is for setting up and tearing down things that need to be done once for each test function.
# It initializes the browser, logs in, and then quits the browser after the test is done.
@pytest.fixture(scope="function")
def oneTimeSetUp(request, browser):
    print("Running one time setUp")

    # Initializing the WebDriver instance for the specified browser
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()

    # Logging into the application
    #lp = LoginPage(driver)
    #lp.login(email="wabcdetest@gmail.com", password="###abc123ABC", username="wabbcdetest")

    # Associating the driver with the current test class, if available
    if request.cls is not None:
        request.cls.driver = driver

    yield driver  # This is where the test function will execute

    # Quitting the browser
    driver.quit()
    print("Running one time tearDown")


# Adding command line options for pytest to specify browser and OS type
def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--osType", help="Type of operating system")


# This fixture returns the browser type specified from the command line (or default if none specified)
@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


# This fixture returns the OS type specified from the command line (or default if none specified)
@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")

