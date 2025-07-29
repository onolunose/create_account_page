

#base/webdriverfactory.py
import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

class WebDriverFactory:
    """
    WebDriver Factory that prefers a local driver .
    Looks for chromedriver/geckodriver in:
      1) Environment variables: CHROMEDRIVER_PATH / GECKODRIVER_PATH
      2) Local folders: ./drivers/, ./bin/, or project root
      3) System PATH (shutil.which)
    If none found, it falls back to Selenium Manager auto-resolution.
    """

    def __init__(self, browser="chrome", headless=False):
        self.browser = (browser or "chrome").lower()
        self.headless = bool(headless)

    def _resolve_driver(self, name: str):
        """Return absolute path to driver if found, else None."""
        env_var = f"{name.upper()}DRIVER_PATH"  # CHROMEDRIVER_PATH / GECKODRIVER_PATH
        candidate = os.getenv(env_var)
        if candidate and os.path.isfile(candidate):
            return candidate

        # Common local locations
        cwd = os.getcwd()
        names = []
        if name == "chrome":
            names = ["chromedriver.exe", "chromedriver"]
        elif name == "gecko":
            names = ["geckodriver.exe", "geckodriver"]

        for folder in ["drivers", "bin", "."]:
            for n in names:
                p = os.path.join(cwd, folder, n) if folder != "." else os.path.join(cwd, n)
                if os.path.isfile(p):
                    return p

        # System PATH
        exe = "chromedriver" if name == "chrome" else "geckodriver"
        which = shutil.which(exe)
        if which:
            return which

        return None

    def getWebDriverInstance(self):
        base_url = os.getenv("BASE_URL", "https://dev-verbatimly.onrender.com/en")

        if self.browser == "chrome":
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--window-size=1440,900")

            path = self._resolve_driver("chrome")
            if path:
                driver = webdriver.Chrome(service=ChromeService(path), options=options)
            else:
                # Fallback to Selenium Manager (may download if not present)
                driver = webdriver.Chrome(options=options)

        elif self.browser == "firefox":
            options = webdriver.FirefoxOptions()
            if self.headless:
                options.add_argument("--headless")

            path = self._resolve_driver("gecko")
            if path:
                driver = webdriver.Firefox(service=FirefoxService(path), options=options)
            else:
                driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")

        driver.implicitly_wait(10)
        try:
            driver.maximize_window()
        except Exception:
            pass
        driver.get(base_url)
        return driver, {"base_url": base_url}
