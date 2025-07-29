# tests/conftest.py
import pytest
from base.webdriverfactory import WebDriverFactory

# ---------------- CLI options ----------------
def pytest_addoption(parser):
    parser.addoption("--browser",  action="store", default="chrome",
                     help="Browser to run: chrome | firefox")
    parser.addoption("--headless", action="store_true",
                     help="Run headless")

# ---------------- Simple fixtures ------------
@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def headless(request):
    return request.config.getoption("--headless")

# Keep your existing 'setUp' usage (no-op fixture)
@pytest.fixture()
def setUp():
    yield

# ---------------- Driver factory -------------
@pytest.fixture(scope="function")
def driver_and_cfg(request, browser, headless):
    """
    Creates a WebDriver per test using your WebDriverFactory and returns (driver, cfg).
    Closes the driver after the test.
    """
    wdf = WebDriverFactory(browser=browser, headless=headless)
    driver, cfg = wdf.getWebDriverInstance()

    # expose on test class if present
    if request.cls:
        request.cls.driver = driver
        request.cls.cfg = cfg

    yield driver, cfg
    driver.quit()


@pytest.fixture(scope="function")
def driver(driver_and_cfg):
    """
    Thin wrapper so tests can simply ask for `driver`.
    """
    drv, _ = driver_and_cfg
    return drv
