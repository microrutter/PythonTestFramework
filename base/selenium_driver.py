import logging
import os
import time
from traceback import print_stack
from selenium.common.exceptions import *
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from utilities.util import Util
import utilities.custom_logger as cl

"""
Selenium driver wrapper for the more common selenium ctions
"""
"""
:Owner:
:Company:
"""
"""
1. **screen_shot** - Takes a string as an argument and creates a screenshot with that name saves it in the screenshot folder in the working directory
(jump to section in [[selenium_driver.py#screen_shot]])

2. **get_title** - Gets the title of the page and returns it as string
(jump to section in [[selenium_driver.py#get_title]])

3. **get_current_url** - Gets the url of the page and returns it as string
(jump to section in [[selenium_driver.py#get_current_url]])

4. **get_element** - Looks for the given locator via the given by type and returns WebElement
(jump to section in [[selenium_driver.py#get_element]])

5. **check_element_exists** - Tries to look for the element via the given locator and By type returns true if found
(jump to section in [[selenium_driver.py#check_element_exists]])

6. **element_click** - Tries to click on a element via given locator and By type
(jump to section in [[selenium_driver.py#element_click]])

7. **send_keys** - Takes a string and sends that to an input element
(jump to section in [[selenium_driver.py#send_keys]])

8. **clear_field** - Clears an input area of any text
(jump to section in [[selenium_driver.py#clear_field]])

9. **wait_for_element** - Waits for an element to become clickable
(jump to section in [[selenium_driver.py#wait_for_element]])

10. **web_scroll** - Scrolls the page up or down by a set amount 
(jump to section in [[selenium_driver.py#web_scroll]])

11. **iframe_switch** - Switches between iframes depending on given arguments
(jump to section in [[selenium_driver.py#iframe_switch]])

12. **alert** - Accepts or declines a javascript alert popup
(jump to section in [[selenium_driver.py#alert]])

13. **alert_text** - Gets the text from a javascript popup alert and returns the text
(jump to section in [[selenium_driver.py#alert_text]])

14. **select_option_text** - Select an option in a select element via visible text
(jump to section in [[selenium_driver.py#select_option_text]])

15. **get_options** - Returns a list of all the options within a select element
(jump to section in [[selenium_driver.py#get_options]])

16. **get_selected_option** - Returns the selected option as WebElement
(jump to section in [[selenium_driver.py#get_selected_option]])

"""
"""
*Internal Methods*

1. **__get_by_type__** - Takes a string and converts that string to type of By and returns this type
(jump to section in [[selenium_driver.py#get_by_type]])

"""

class SeleniumDriver:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    # === screen_shot ===
    def screen_shot(self, result_message :str):
        file_name = result_message + "." + str(round(time.time() * 1000)) + ".png"
        screenshot_directory = "../screenshots/"
        relative_file_name = screenshot_directory + file_name
        current_directory = os.path.dirname(__file__)
        destination_file = os.path.join(current_directory, relative_file_name)
        destination_directory = os.path.join(current_directory, screenshot_directory)
        try:
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
            self.driver.save_screenshot(destination_file)
            self.log.info("Screenshot save to directory: " + destination_file)
        except:
            self.log.error("### Exception Occurred when taking screenshot")

    # === get_title ===
    def get_title(self) -> str:
        return self.driver.title

    # === get_current_url ===
    def get_current_url(self) -> str:
        return self.driver.current_url

    # === get_by_type === 
    def __get_by_type__(self, locator_type: str) -> By:
        locator_type = locator_type.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locator_type + " not correct/supported")
        return False

    # === get_element ===
    def get_element(self, locator: str, locator_type: str="id", element: WebElement = None) -> WebElement:
        element_return = None
        try:
            locator_type = locator_type.lower()
            by_type = self.__get_by_type__(locator_type)
            if element is not None:
                element_return = element.find_element(by_type, locator)
                self.log.info(
                    "Element found with locator: "
                    + locator
                    + " and  locator_type: "
                    + locator_type
                )
            else:
                element_return = self.driver.find_element(by_type, locator)
                self.log.info(
                    "Element found with locator: "
                    + locator
                    + " and  locator_type: "
                    + locator_type
                )
        except:
            self.log.error(
                "Element not found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            self.screen_shot("Element_not_found_" + locator)
        return element_return

    # === check_element_exists ===
    def check_element_exists(self, locator: str, locator_type: str="id") -> bool:
        try:
            locator_type = locator_type.lower()
            by_type = self.__get_by_type__(locator_type)
            self.driver.find_element(by_type, locator)
            self.log.info(
                "Element found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            return True
        except:
            self.log.error(
                "Element not found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            return False

    # === element_click ===
    def element_click(self, locator: str, locator_type: str="id", element: WebElement=None):
        try:
            if element is not None:
                element_sub = self.get_element(locator=locator, locator_type=locator_type, element=element)
                element_sub.click()
                self.log.info("Clicked on sub element with locator: "
                + locator
                + " locator type: "
                + locator_type)
            else:
                element_main = self.get_element(locator, locator_type)
                element_main.click()
                self.log.info(
                    "Clicked on element with locator: "
                    + locator
                    + " locator type: "
                    + locator_type
                )
            Util.sleep(Util, sec=1, info="Give page time to react")
        except:
            self.log.error(
                "Cannot click on the element with locator: "
                + locator
                + " locator_type: "
                + locator_type
            )
            self.screen_shot("Element_click_not_found_" + locator)
            print_stack()

    # === send_keys ===
    def send_keys(self, data: str, locator: str, locator_type: str="id", element: WebElement=None):
        try:
            if element is not None:
                element_sub = self.get_element(locator=locator, locator_type=locator_type, element=element)
                element_sub.send_keys(data)
                self.log.info(
                    "Sent data on sub element with locator: "
                    + locator
                    + " locator_type: "
                    + locator_type
                )
            else:
                element_main = self.get_element(locator=locator, locator_type=locator_type)
                element_main.send_keys(data)
                self.log.info(
                    "Sent data on main element with locator: "
                    + locator
                    + " locator_type: "
                    + locator_type
                )
        except:
            self.log.error(
                "Cannot send data on the element with locator: "
                + locator
                + " locator_type: "
                + locator_type
            )
            self.screen_shot("Element_send_keys_not_found_" + locator)
            print_stack()

    # === clear_field ===
    def clear_field(self, locator: str, locator_type: str="id"):
        element = self.get_element(locator, locator_type)
        element.clear()
        self.log.info(
            "Clear field with locator: " + locator + " locator_type: " + locator_type
        )

    # === wait_for_element ===
    def wait_for_element(
        self, locator: str, locator_type: str="id", timeout: int=10, poll_frequency: float=0.5
    ) -> bool:
        element = None
        try:
            by_type = self.__get_by_type__(locator_type)
            self.log.info(
                "Waiting for maximum :: "
                + str(timeout)
                + " :: seconds for element to be clickable"
            )
            wait = WebDriverWait(
                self.driver,
                timeout=timeout,
                poll_frequency=poll_frequency,
                ignored_exceptions=[
                    NoSuchElementException,
                    ElementNotVisibleException,
                    ElementNotSelectableException,
                ],
            )
            element = wait.until(EC.element_to_be_clickable((by_type, locator)))
            self.log.info("Element appeared on the web page")
            return True
        except:
            self.log.error("Element not appeared on the web page")
            self.screen_shot("Element_not_found_" + locator)
            print_stack()
            return False
    
    # === web_scroll ===
    def web_scroll(self, direction: str="up"):
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")

    # === iframe_switch ===
    def iframe_switch(self, parent: str="yes", string: str="no", num: int=0):
        if parent == "yes":
            self.driver.switch_to.default_content()
        elif string == "no":
            self.driver.switch_to.frame(num)
        else:
            self.driver.switch_to.frame(string)

    # === alert ===
    def alert(self, accept: str="yes"):
        alert = self.driver.switch_to.alert
        if accept == "yes":
            alert.accept()
        else:
            alert.dismiss()
    
    # === alert_text ===
    def alert_text(self) -> str:
        Util.sleep(Util, sec=2, info="Give alert time to react")
        try:
            alert = self.driver.switch_to.alert
            return alert.text
        except Exception as e:
            self.log.info(e)
            
    # === select_option_text ===
    def select_option_text(self, text: str, locator: str, locator_type: str="id"):
        try:
            select = Select(self.get_element(locator, locator_type))
            # select by visible text
            select.select_by_visible_text(text)
            self.log.info("Select option found and selected")
        except:
            self.log.error("Select option not found")

    # === get_options ===
    def get_options(self, locator: str, locator_type: str="id") -> list:
        try:
            select = Select(self.get_element(locator, locator_type))
            self.log.info("Select option found and selected")
            return select.options
        except:
            self.log.error("Select option not found")
   
    # === get_selected_option ===
    def get_selected_option(self, locator: str, locator_type: str="id") -> WebElement:
        try:
            select = Select(self.get_element(locator, locator_type))
            self.log.info("Select found and option selected returned")
            return select.first_selected_option
        except:
            self.log.info("Select option not found")
