import logging
import time
import re
from bs4 import BeautifulSoup
from utilities.util import Util

import utilities.custom_logger as cl

"""
BeautifulSoup helpers uses beautifulsoup to navigate the DOM to help get text
navigate tables and find buttons intended as an extension to selenium methods
"""
"""
:Author: Wayne
"""
"""
1. **get_text_all** - Looks for a given element and returns the text of that element and all child elements
(jump to section in [[beautifulsouphelpers.py#get_text_all]])

2. **get_text_element_sibling** - Looks for a given element and the given children of that element and returns thier text
(jump to section in [[beautifulsouphelpers.py#get_text_element_sibling]])

3. **count_sibling** - Looks for a given element and counts how many of a given sibling that element contains
(jump to section in [[beautifulsouphelpers.py#count_sibling])

4. **get_attribute_button** - Returns the value of a given attribute
(jump to section in [[beautifulsouphelpers.py#]])

5. **get_table_rows** - Gets all the rows belonging in a table only use this if one table on page.
(jump to section in [[beautifulsouphelpers.py#get_table_rows]])

6. **search_row_for_element** - Takes a list of table rows and searches for a given element if element is found will return that row
(jump to section in [[beautifulsouphelpers.py#search_row_for_element]])

7. **get_all_sibling_divs** - Looks for a given element and returns all child divs
(jump to section in [[beautifulsouphelpers.py#get_all_sibling_divs]])

8. **get_attribute_button** - Looks for a given element and returns the elements attributes
(jump to section in [[beautifulsouphelpers.py#get_attribute_button]])

9. **find_clickable_element** - Looks for a clickable element (not anchor) with a given value and returns that elements attributes as list
(jump to section in [[beautifulsouphelpers.py#find_clickable_element]])

10. **find_clickable_element_sibling** - As above but this is given a beautifulsoup object to find the clickable elements in
(jump to section in [[beautifulsouphelpers.py#find_clickable_element_sibling]])

11. **find_clickable_element_partial_text** - Looks for a possible clickable element that match's a partial text and returns that elements attributes as list
(jump to section in [[beautifulsouphelpers.py#find_clickable_element_partial_text]])

12. **get_text** - Returns the text of a specific element
(jump to section in [[beautifulsouphelpers.py#get_text]])

13. **get_anchor_elements** - Returns the text and href of all anchor elements within a given page
(jump to section in [[beautifulsouphelpers.py#get_all_anchors]])
"""


class Helpers:

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, section):
        self.bs = BeautifulSoup(section, "html5lib")
        self.util = Util()
    
    # ===get_all_anchors===
    def get_anchor_elements(self) -> list:
        urls: list = []
        for a in self.bs.find_all('a'):
            urls.append(dict(text=a.get_text(), link=a['href']))
        return urls

    # ===get_text_all===
    def get_text_all(self, tag: str = "", attributes: dict = {}) -> str:
        elements = self.bs.find_all(tag, attributes)
        result = ""
        for element in elements:
            result = result + element.get_text() + " "
        return result
    
    # ===get_text===
    def get_text(self, tag: str = "", attributes: dict = {}) -> str:
        element = self.bs.find(tag, attributes)
        return element.get_text()

    # ===get_text_element_sibling===
    def get_text_element_sibling(
        self,
        tag: str = "",
        attributes: dict = {},
        sib_tag: str = "",
        sib_attributes: dict = {},
    ) -> str:
        parent = self.bs.find(tag, attributes)
        elements = parent.find_all(sib_tag, sib_attributes)
        result = ""
        for element in elements:
            result = result + element.get_text() + " "
        return result

    # ===count_sibling===
    def count_sibling(
        self,
        tag: str = "",
        attributes: dict = {},
        sib_tag: str = "",
        sib_attributes: dict = {},
        sib_text: str = None,
    ) -> int:
        self.util.sleep(2)
        parent = self.bs.find(tag, attributes)
        if sib_text:
            elements = parent.find_all(sib_tag, text=sib_text)
        else:
            elements = parent.find_all(sib_tag, sib_attributes)
        return len(elements)

    # === get_table_rows ===
    def get_table_rows(self) -> list:
        table = self.bs.find("table")
        tbody = table.find("tbody")
        return tbody.findAll("tr")

    # === search_row_for_element ===
    def search_row_for_element(
        self, rows: list, tag: str, attributes: dict
    ) -> BeautifulSoup:
        for row in rows:
            candidate = row.find(tag, attributes)
            if candidate:
                return row

    # === get_all_sibling_divs ===
    def get_all_sibling_divs(
        self, parent: BeautifulSoup, tag: str, attributes: dict
    ) -> list:
        return parent.find(tag, attributes).findAll("div")

    # ===get_attribute_button===
    @staticmethod
    def get_attribute_button(parent: BeautifulSoup, att: str) -> str:
        button = parent.find("button")
        return button[att]

    # ===find_clickable_element===
    def find_clickable_element(self, text: str = "") -> list:
        button = self.bs.find_all("button")
        input = self.bs.find_all("input")
        if len(button) > 0:
            self.log.info("button length: " + str(len(button)))
            for but in button:
                if self.util.verifyTextMatch(actualText=re.sub(r"\s+", "", but.get_text()), expectedText=re.sub(r"\s+", "", text)):
                    return ["button", but]
        if len(input) > 0:
            self.log.info("input length: " + str(len(input)))
            for but in input:
                if but.has_attr('value'):
                    if self.util.verifyTextMatch(actualText=but["value"], expectedText=text):
                        return ["input", but]
        return None

    # ===find_clickable_element_sibling===
    def find_clickable_element_sibling(self, text: str, parent: BeautifulSoup) -> list:
        button = parent.find_all("button")
        input = parent.find_all("input")
        if len(button) > 0:
            for but in button:
                if self.util.verifyTextMatch(actualText=re.sub(r"\s+", "", but.get_text()), expectedText=re.sub(r"\s+", "", text)):
                    return ["button", but]
        if len(input) > 0:
            for but in input:
                if but.has_attr('value'):
                    if self.util.verifyTextMatch(actualText=but["value"], expectedText=text):
                        return ["input", but]
        return None
    
    # ===find_clickable_element_partial_text===
    def find_clickable_element_partial_text(self, partialtext: str = "") -> list:
        button = self.bs.find_all("button")
        input = self.bs.find_all("input")
        if len(button) > 0:
            for but in button:
                if self.util.verifyTextContains(actualText=but.get_text(), expectedText=partialtext):
                    return ["button", but]
        if len(input) > 0:
            for but in input:
                if but.has_attr('value'):
                    if self.util.verifyTextContains(actualText=but["value"], expectedText=partialtext):
                        return ["input", but]
        return None
