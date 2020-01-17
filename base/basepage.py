"""
@package base

Base Page class implementation
It implements methods which are common to all the pages throughout the application

This class needs to be inherited by all the page classes
This should not be used by creating object instances

Example:
    Class LoginPage(BasePage)
"""
import time
from traceback import print_stack
import logging
from base.beautifulsouphelpers import Helpers as bh
from base.selenium_driver import SeleniumDriver
from utilities.util import Util
import utilities.custom_logger as cl


class BasePage(SeleniumDriver):

    log = cl.customLogger(logging.DEBUG)

    _save = "save"
    _delete = "delete"

    def __init__(self, driver):
        """
        Inits BasePage class

        Returns:
            None
        """
        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()
        self.bh = bh

    def verify_page_title(self, title_to_verify):
        """
        Verify the page Title

        Parameters:
            title_to_verify: Title on the page that needs to be verified
        """
        try:
            actual_title = self.get_title()
            return self.util.verifyTextContains(actual_title, title_to_verify)
        except:
            self.log.error("Failed to get page title")
            print_stack()
            return False

    """
    """

    def css_builder(self, element) -> str:
        css_build = ""
        for at in element.attrs:
            value = element[at]
            css_build = css_build + "[" + at + "="
            if isinstance(value, str):
                css_build = css_build + "'" + value
            else:
                l = len(value)
                i = 1
                for v in value:
                    if i == 1:
                        css_build = css_build + "'" + v + ""
                    else:
                        css_build = css_build + " " + v + ""
                    i = i + 1
            css_build = css_build + "']"
        return css_build

    """
        Search's for the exact test you give it
        to see if any button elements or
        input elements have that text and then
        will click on that element
    """

    def click_on_button(self, label: str):
        time.sleep(2)
        bs = self.bh(self.driver.page_source)
        button = bs.find_clickable_element(label)
        if len(button) > 0:
            css = self.css_builder(button[1])
            self.log.info(button[0] + css)
            self.element_click(button[0] + css, "css")
        else:
            self.screen_shot(result_message="button_not_found")

    """
        Search's for the exact text you give it
        to see if any button elements or
        input elements have that text and then
        will click on that element and return the css
        of the given element
    """

    def click_on_button_return_parent_css(self, label: str) -> str:
        time.sleep(2)
        bs = self.bh(self.driver.page_source)
        button = bs.find_clickable_element(label)
        if len(button) > 1:
            css = self.css_builder(button[1])
            css_return = self.css_builder(button[1].parent)
            self.log.info(button[0] + css)
            self.element_click(button[0] + css, "css")
            return button[1].parent.name + css_return
        else:
            self.screen_shot(result_message="button_not_found")

    """
        Click on Delete button
    """

    def click_on_delete_button(self):
        self.click_on_button(label="Delete")
        time.sleep(3)
        alert_obj = self.driver.switch_to.alert
        alert_obj.accept()

    """
        Click on Delete button return css
    """

    def click_on_delete_button_return_css(self) -> str:
        css = self.click_on_button_return_parent_css(label="Delete")
        time.sleep(3)
        alert_obj = self.driver.switch_to.alert
        alert_obj.accept()
        return css

    def scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait to load page
            time.sleep(0.5)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
