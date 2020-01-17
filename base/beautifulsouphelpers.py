import logging
import time
import re
from bs4 import BeautifulSoup

import utilities.custom_logger as cl

"""
BeautifulSoup helpers uses beautifulsoup to navigate the DOM to help get text
navigate tables and find buttons intended as an extension to selenium methods
"""
"""
:Owner:
:Company:
"""
"""
1. **get_text_all** - Returns all text of all elements
(jump to section in [[beautifulsouphelpers.py#text_all]])

2. **get_text_element_sibling** - Returns all text of all child elements
(jump to section in [[beautifulsouphelpers.py#child_text]])

3. **count_sibling** - Returns length of elements found
(jump to section in [[beautifulsouphelpers.py#count_elements]])

4. **get_parent_with_tag_and_text** - Returns BeautifulSoup object
(jump to section in [[beautifulsouphelpers.py#parent_search]])

5. **get_parent_text** - Returns string of parent
(jump to section in [[beautifulsouphelpers.py#parent_text]])

6. **get_attribute_button** - Returns the value of a given attribute
(jump to section in [[beautifulsouphelpers.py#]])
"""


class Helpers:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, section):
        self.bs = BeautifulSoup(section, "html5lib")

    # ===text_all===
    def get_text_all(self, tag: str = "", attributes: dict = {}) -> str:
        """
        Finds all the elements matching the given parameters then gets the text
        from each element and adds it to a string which it then returns.
        :Author: Wayne Rutter
        :Params: tag string element tag (a, input, button, div, etc)
        :Params: attributes dict elements attributes ({'class': 'container'})
        :Returns: String
        """
        elements = self.bs.find_all(tag, attributes)
        result = ""
        for element in elements:
            result = result + element.get_text() + " "
        return result

    # ===child_text===
    def get_text_element_sibling(
        self,
        tag: str = "",
        attributes: dict = {},
        sib_tag: str = "",
        sib_attributes: dict = {},
    ) -> str:
        """
        Finds the parent element matching the given parameters then gets all
        the matching child elements text and adds it to a string which it then
        returns.
        :Author: Wayne Rutter
        :Params: tag string element tag (a, input, button, div, etc)
        :Params: attributes dict elements attributes ({'class': 'container'})
        :Params: sib_tag string child element tag
        :Params: sib_attributes dict child elements attributes
        :Returns: String
        """
        parent = self.bs.find(tag, attributes)
        elements = parent.find_all(sib_tag, sib_attributes)
        result = ""
        for element in elements:
            result = result + element.get_text() + " "
        return result

    # ===count_elements===
    def count_sibling(
        self,
        tag: str = "",
        attributes: dict = {},
        sib_tag: str = "",
        sib_attributes: dict = {},
        sib_text: str = None,
    ) -> int:
        """
        Finds the parent element then looks for any child elements that match
        the search criteria returns the number of elements that match.
        :Author: Wayne Rutter
        :Params: tag string element tag (a, input, button, div, etc)
        :Params: attributes dict elements attributes ({'class': 'container'})
        :Params: sib_tag string child element tag
        :Params: sib_attributes dict child elements attributes
        :Params: sib_text string search for element depending on its value
        :Returns: String
        """
        time.sleep(2)
        parent = self.bs.find(tag, attributes)
        if sib_text:
            elements = parent.find_all(sib_tag, text=sib_text)
        else:
            elements = parent.find_all(sib_tag, sib_attributes)
        return len(elements)

    # ===parent_search===
    def get_parent_with_tag_and_text(
        self, tag: str = "", attributes: str = "", parent_element: str = ""
    ) -> BeautifulSoup:
        """
        Finds the parent of an element and returns the BeautifulSoup object
        :Author: Wayne Rutter
        :Params: tag string element tag (a, input, button, div, etc)
        :Params: attributes string element value to search for
        :Params: parent_element string the tag of the parent to find ('div')
        :Returns: BeautifulSoup object
        """
        child = self.bs.find(tag, text=attributes)
        self.log.info(child)
        return child.find_parent(parent_element)

    # ===parent_text===
    def get_parent_text(self, tag: str = "", attributes: dict = "") -> str:
        """
        Finds the value of the immediate parent of a child element
        :Author: Wayne Rutter
        :Params: tag string element tag (a, input, button, div, etc)
        :Params: attributes dict elements attributes ('class': 'container')
        :Returns: String
        """
        child = self.bs.find(tag, attributes)
        return child.parent.get_text()

    # ===button_att===
    @staticmethod
    def get_attribute_button(parent: BeautifulSoup, att: str) -> str:
        """
        Finds the first button element within the parent and returns the value
        of the given attribute
        :Author: Wayne Rutter
        :Params: parent BeautifulSoup Object
        :Params: str string
        :Returns: String
        """
        button = parent.find("button")
        return button[att]

    @staticmethod
    def get_text_button(parent) -> str:
        button = parent.find("button")
        return button.get_text()

    @staticmethod
    def get_text_strong(parent) -> str:
        strong = parent.find("strong")
        return strong.get_text()

    @staticmethod
    def get_text(parent) -> str:
        return parent.get_text()

    def check_element_exists(self, tag: str = "", attributes: dict = {}) -> bool:
        element = self.bs.find(tag, attributes)
        return element["style"]

    def get_all_options(self) -> list:
        options = []
        for option in self.bs.find_all("option"):
            options.append(option.get_text())
        return options

    def get_all_disabled_elements(self) -> list:
        inputs = self.bs.find_all("input", {"type": "text"})
        selects = self.bs.find_all("select")
        self.log.info("Length of inputs: " + str(len(inputs)))
        self.log.info("Length of selects: " + str(len(selects)))
        disabled_list = []
        for inp in inputs:
            if "disabled" in inp.attrs:
                disabled_list.append(inp)
        for select in selects:
            if select.has_attr("disabled"):
                disabled_list.append(select)
        return disabled_list

    def get_element(self, tag: str = "", attributes: dict = ""):
        return self.bs.find(tag, attributes)

    def get_element_parent_list(self, tag: str = "", attributes: dict = "", parent=""):
        return parent.find_all(tag, attributes)

    @staticmethod
    def check_element_in_list(bs_list: list, attr: str) -> bool:
        for element in bs_list:
            if str(element["id"]) == attr:
                return True
        else:
            return False

    # Under construction
    def find_clickable_element(self, text: str = ""):
        button = self.bs.find_all("button")
        input = self.bs.find_all("input")
        if len(button) > 0:
            print("in button")
            for but in button:
                if re.sub(r"\s+", "", but.get_text()) == re.sub(r"\s+", "", text):
                    return ["button", but]
        if len(input) > 0:
            print("in input")
            for but in input:
                print(but["value"])
                if but["value"] == text:
                    return ["input", but]
        return None
