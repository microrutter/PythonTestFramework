"""
@package base

WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""

import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class WebDriverFactory:
    def __init__(self, browser):
        """
        Inits WebDriverFactory class

        Returns:
            None
        """
        self.browser = browser

    """
        Set chrome driver and iexplorer environment based on OS

        chromedriver = "C:/.../chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

        PREFERRED: Set the path on the machine where browser will be executed
    """

    def get_web_driver_instance(
        self,
        url="",
        server="",
    ):
        """
       Get WebDriver Instance based on the browser configuration

        Returns:
            'WebDriver Instance'
        """
        base_url = url
        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
            # Maximize the window
            driver.maximize_window()
        elif self.browser == "firefox":
            driver = webdriver.Firefox(
                executable_path=os.path.join(os.getcwd(), "base/drivers/geckodriver")
            )
            # Maximize the window
            driver.maximize_window()
        elif self.browser == "chrome":
            # Set chrome driver
            print(os.getcwd())
            chromedriver = os.path.join(os.getcwd(), "base/drivers/chromedriver")
            os.environ["webdriver.chrome.driver"] = chromedriver
            driver = webdriver.Chrome(chromedriver)
            # Maximize the window
        elif self.browser == "remoteChrome":
            driver = webdriver.Remote(
                command_executor="http://" + server + ":4444/wd/hub",
                desired_capabilities=DesiredCapabilities.CHROME,
            )
        else:
            driver = webdriver.Remote(
                command_executor="http://" + server + ":4444/wd/hub",
                desired_capabilities=DesiredCapabilities.FIREFOX,
            )

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(3)

        # Loading browser with App URL
        driver.get(base_url)
        return driver
