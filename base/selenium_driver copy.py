import logging
import os
import time
from traceback import print_stack

from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

import utilities.custom_logger as cl


class SeleniumDriver:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    # Takes screen shot of current page
    def screen_shot(self, result_message):
        """
        Takes screenshot of the current open web page
        """
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
            print_stack()

    # gets the title of the page
    def get_title(self):
        return self.driver.title

    # gets the current url of the page
    def get_current_url(self):
        return self.driver.current_url

    # Returns By type
    def get_by_type(self, locator_type):
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

    # gets element dependent on type
    def get_element(self, locator, locator_type="id"):
        """
        returns the element
        :param locator:
        :param locator_type:
        :return:
        """
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_element(by_type, locator)
            self.log.info(
                "Element found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
        except:
            self.log.info(
                "Element not found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            self.screen_shot("Element_not_found_" + locator)
        return element

    # gets element dependent on type
    def check_element_exists(self, locator, locator_type="id"):
        """
        returns True if element exists
        :param locator:
        :param locator_type:
        :return:
        """
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            self.driver.find_element(by_type, locator)
            self.log.info(
                "Element found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            return True
        except:
            self.log.info(
                "Element not found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            return False

    # gets element dependent on type
    def check_web_element_exists(self, element_w, locator, locator_type="id"):
        """
        returns True if element exists
        :param element_w:
        :param locator:
        :param locator_type:
        :return:
        """
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element_w.find_element(by_type, locator)
            self.log.info(
                "Element found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            return True
        except:
            self.log.info(
                "Element not found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            return False

    # gets element dependent on type
    def get_web_element(self, element_w, locator, locator_type="id"):
        """
        returns the element
        :param element_w:
        :param locator:
        :param locator_type:
        :return:
        """
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = element_w.find_element(by_type, locator)
            self.log.info(
                "Element found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            return element
        except:
            self.log.info(
                "Element not found with locator: "
                + locator
                + " and  locator_type: "
                + locator_type
            )
            self.screen_shot("Element_not_found_" + locator)
            return None

    # gets element list
    def get_element_list(self, locator, locator_type="id"):
        """
        NEW METHOD
        Get list of elements
        """
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = self.driver.find_elements(by_type, locator)
            self.log.info(
                "Element list found with locator: "
                + locator
                + " and locator_type: "
                + locator_type
            )
        except:
            self.log.info(
                "Element list not found with locator: "
                + locator
                + " and locator_type: "
                + locator_type
            )
            self.screen_shot("Element_list_not_found_" + locator)
        return element

    # gets element list
    def get_web_element_list(self, element_w, locator="", locator_type="id"):
        """
        Get webelement list
        :param element_w:
        :param locator:
        :param locator_type:
        :return:
        """
        self.log.info("Checking list: " + element_w.get_attribute("class"))
        element = None
        try:
            locator_type = locator_type.lower()
            by_type = self.get_by_type(locator_type)
            element = element_w.find_elements(by_type, locator)
            self.log.info(
                "Element list found with locator: "
                + locator
                + " and locator type: "
                + locator_type
            )
            return element
        except:
            self.log.info(
                "Element list not found with locator: "
                + locator
                + " and locator type: "
                + locator_type
                + " and element "
                + element_w
            )
            self.log.info(print_stack())
            self.screen_shot("Element list not found" + locator)
            return None

    # clicks on specified element
    def element_click(self, locator="", locator_type="id", element=None):
        """
        Click on an element -> MODIFIED
        Either provide element or a combination of locator and locator type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            element.click()
            self.log.info(
                "Clicked on element with locator: "
                + locator
                + " locator type: "
                + locator_type
            )
            time.sleep(1)
        except:
            self.log.info(
                "Cannot click on the element with locator: "
                + locator
                + " locator_type: "
                + locator_type
            )
            self.screen_shot("Element_click_not_found_" + locator)
            print_stack()

    # clicks on specified element
    def element_web_click(self, element_w, locator="", locator_type="id", element=None):
        """
        Click on an element -> MODIFIED
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                self.wait_for_element_ele(element_w, locator, locator_type)
                element = self.get_web_element(element_w, locator, locator_type)
            element.click()
            self.log.info(
                "Clicked on element with locator: "
                + locator
                + " locator_type: "
                + locator_type
            )
        except:
            try:
                element_w.click()
            except:
                self.log.info(
                    "Cannot click on the element with locator: "
                    + locator
                    + " locator_type: "
                    + locator_type
                )
                self.log.info(print_stack())
                self.screen_shot("Element_click_not_found_" + locator)

    def send_keys(self, data, locator="", locator_type="id", element=None):
        """
        Send keys to an element -> MODIFIED
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            element.send_keys(data)
            self.log.info(
                "Sent data on element with locator: "
                + locator
                + " locator_type: "
                + locator_type
            )
        except:
            self.log.info(
                "Cannot send data on the element with locator: "
                + locator
                + " locator_type: "
                + locator_type
            )
            self.screen_shot("Element_send_keys_not_found_" + locator)
            print_stack()

    def clear_field(self, locator="", locator_type="id"):
        """
        Clear an element field
        """
        element = self.get_element(locator, locator_type)
        element.clear()
        self.log.info(
            "Clear field with locator: " + locator + " locator_type: " + locator_type
        )

    def get_text(self, locator="", locator_type="id", element=None, info=""):
        """
        NEW METHOD
        Get 'Text' on an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            self.screen_shot("Element_text_not_found_" + locator)
            text = None
        return text

    def get_web_element_text(
        self, webele, locator="", locator_type="id", element=None, info=""
    ):
        """
        NEW METHOD
        Get 'Text' on an element
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_web_element(webele, locator, locator_type)
            text = element.text
            self.log.info("The text is :: '" + text + "'")
            if len(text) == 0:
                text = element.get_attribute("innerText")
                self.log.info("The text is :: '" + text + "'")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            self.screen_shot("Element_text_not_found_" + locator)
            text = None
        return text

    def is_element_present(self, locator="", locator_type="id", element=None):
        """
        Check if element is present -> MODIFIED
        Either provide element or a combination of locator and locator_type
        """
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            if element is not None:
                self.log.info(
                    "Element present with locator: "
                    + locator
                    + " locator_type: "
                    + locator_type
                )
                return True
            else:
                self.log.info(
                    "Element not present with locator: "
                    + locator
                    + " locator_type: "
                    + locator_type
                )
                return False
        except:
            print("Element not found")
            return False

    def is_element_displayed(self, locator="", locator_type="id", element=None):
        """
        NEW METHOD
        Check if element is displayed
        Either provide element or a combination of locator and locator_type
        """
        is_displayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.get_element(locator, locator_type)
            if element is not None:
                is_displayed = element.is_displayed()
                self.log.info("Element is displayed")
            else:
                self.log.info("Element not displayed")
            return is_displayed
        except:
            print("Element not found")
            return False

    def element_presence_check(self, locator, by_type="id"):
        """
        Check if element is present
        """
        try:
            element_list = self.driver.find_elements(by_type, locator)
            if len(element_list) > 0:
                self.log.info(
                    "Element present with locator: "
                    + locator
                    + " locator_type: "
                    + str(by_type)
                )
                return True
            else:
                self.log.info(
                    "Element not present with locator: "
                    + locator
                    + " locator_type: "
                    + str(by_type)
                )
                return False
        except:
            self.log.info("Element not found")
            return False

    def wait_for_element(
        self, locator, locator_type="id", timeout=10, poll_frequency=0.5
    ):
        """
        Waits for element to appear
        :param locator:
        :param locator_type:
        :param timeout:
        :param poll_frequency:
        :return:
        """
        element = None
        try:
            by_type = self.get_by_type(locator_type)
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
            self.log.info("Element not appeared on the web page")
            self.screen_shot("Element_not_found_" + locator)
            print_stack()
            return False

    def wait_for_element_ele(
        self, ele, locator, locator_type="id", timeout=10, poll_frequency=0.5
    ):
        """
        Waits for element to appear
        :param locator:
        :param locator_type:
        :param timeout:
        :param poll_frequency:
        :return:
        """
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            self.log.info(
                "Waiting for maximum :: "
                + str(timeout)
                + " :: seconds for element to be clickable"
            )
            wait = WebDriverWait(
                ele,
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
        except:
            self.log.info("Element not appeared on the web page")
            self.screen_shot("Element_not_found_" + locator)
            print_stack()
        return element

    def web_scroll(self, direction="up"):
        """
        Scrolls page up or down
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")

    def iframe_switch(self, parent="yes", str="no", num=0):
        """
        Switch's between iframes
        using either id, name or number of
        iframe
        :return:
        """
        if parent == "yes":
            self.driver.switch_to.default_content()
        elif str == "no":
            self.driver.switch_to.frame(num)
        else:
            self.driver.switch_to.frame(str)

    def alert(self, accept="yes"):
        """
        switch to alert and
        either accept or dismiss
        :return:
        """
        alert = self.driver.switch_to.alert
        if accept == "yes":
            alert.accept()
        else:
            alert.dismiss()

    def select_option_text(self, text, locator, locator_type="id"):
        """
        Selects option by text
        :param locator:
        :param locator_type:
        :param text:
        """
        try:
            select = Select(self.get_element(locator, locator_type))
            # select by visible text
            select.select_by_visible_text(text)
            self.log.info("Select option found and selected")
        except:
            self.log.info("Select option not found")

    def get_options(self, locator, locator_type="id"):
        """
        Gets Options
        :param locator:
        :param locator_type:
        :param text:
        """
        try:
            select = Select(self.get_element(locator, locator_type))
            # select by visible text
            self.log.info("Select option found and selected")
            return select.options
        except:
            self.log.info("Select option not found")

    def get_selected_option(self, locator, locator_type="id"):
        """
        Gets Selected Options
        :param locator:
        :param locator_type:
        :param text:
        """
        try:
            select = Select(self.get_element(locator, locator_type))
            # select by visible text
            self.log.info("Select found and option selected returned")
            return select.first_selected_option
        except:
            self.log.info("Select option not found")
