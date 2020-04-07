import time
from traceback import print_stack
import logging
from base.beautifulsouphelpers import Helpers as bh
from bs4 import BeautifulSoup
from base.selenium_driver import SeleniumDriver
from utilities.util import Util
import utilities.custom_logger as cl

"""
   Base page is where all pages inherit from and all common methods should be implemented here
"""
"""
:Author: Wayne Rutter
"""
"""
**Base Page Functions:**

1. **verify_page_title** - Verify page title matches given string returns boolean
(jump to section in [[basepage.py#verify_title]] )

2. **css_builder** - Create cssSelector for selenium to find or click element takes BeautifulSoup Element returns String
(jump to section in [[basepage.py#css_builder]])

3. **click_on_button** - Given a string will search elements to find button with that String and click on it
(jump to section in [[basepage.py#click_on_button]])

4. **click_on_button_given_parent** - Given a string and a BeautifulSoup element will search for clickable element within the BeautifulSoup Element
(jump to section in [[basepage.py#click_on_button_given_parent]])

5. **click_on_delete_button_with_alert** - Looks for a button labelled Delete clicks it and handles javascript alert popups
(jump to section in [[basepage.py#click_on_delete_button_with_alert]])

6. **scroll_to_bottom** - Scrolls to the bottom of the page
(jump to section in [[basepage.py#scroll_to_bottom]])

7. **click_on_link** - Clicks on Anchor links
(jump to section in [[basepage.py#click_on_link]])

8. **concate_string** - Takes a list of strings and creates a single string from them and returns that string
(jump to section in [[basepage.py#concate_string]])
"""

class BasePage(SeleniumDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        
        super(BasePage, self).__init__(driver)
        self.driver = driver
        self.util = Util()
        self.bh = bh
    
    # === verify_title ===
    def verify_page_title(self, title_to_verify: str) -> bool:
        try:
            actual_title = self.get_title()
            return self.util.verifyTextContains(actual_title, title_to_verify)
        except:
            self.log.error("Failed to get page title")
            print_stack()
            return False
    
    # === css_builder ===
    def css_builder(self, element: BeautifulSoup) -> str:
        css_build = ""
        for at in element.attrs:
            value = element[at]
            css_build = css_build + "[" + at + "="
            if isinstance(value, str):
                css_build = css_build + "\"" + value
            else:
                l = len(value)
                i = 1
                for v in value:
                    if i == 1:
                        css_build = css_build + "\"" + v + ""
                    else:
                        css_build = css_build + "\"" + v + ""
                    i = i + 1
            css_build = css_build + "\"]"
        return css_build

    # === click_on_button ===
    def click_on_button(self, label: str):
        self.util.sleep(2)
        bs = self.bh(self.driver.page_source)
        button = bs.find_clickable_element(label)
        if len(button) > 0:
            css = self.css_builder(button[1])
            self.log.info(button[0] + css)
            self.element_click(button[0] + css, "css")
        else:
            self.screen_shot(result_message="button_not_found")
    
    # === click_on_button_given_parent ===       
    def click_on_button_given_parent(self, label: str, parent: BeautifulSoup):
        self.util.sleep(2)
        bs = self.bh(self.driver.page_source)
        button = bs.find_clickable_element_sibling(text=label, parent=parent)
        if len(button) > 0:
            css = self.css_builder(button[1])
            self.log.info(button[0] + css)
            self.element_click(button[0] + css, "css")
        else:
            self.screen_shot(result_message="button_not_found")

    # === click_on_delete_button_with_alert ===
    def click_on_delete_button_with_alert(self):
        self.click_on_button(label="Delete")
        self.util.sleep(3)
        alert_obj = self.driver.switch_to.alert
        alert_obj.accept()

    # === scroll_to_bottom ===
    def scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            # Wait to load page
            self.util.sleep(0.5)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    # === click_on_link ===
    def click_on_link(self, displayText: str):
        self.driver.find_element_by_link_text(displayText).click()
    
    # === concate_string ===
    def concate_string(self, createString: list) -> str:
        returnString: str = ""
        for string in createString:
            returnString = returnString + string + " "
        return returnString.rstrip()