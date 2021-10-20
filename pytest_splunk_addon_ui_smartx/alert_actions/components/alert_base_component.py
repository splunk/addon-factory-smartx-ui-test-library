#
# Copyright 2021 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
from collections import namedtuple

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains as action_chains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 20


class ActionChains(action_chains):
    """
    Purpose:
    It is a workaround by wrapping ActionChains class so that key_action.pause is not used in Safari browser.
    """

    def __init__(self, browser):
        super().__init__(browser)
        if browser.name in ("Safari", "Safari Technology Preview"):
            self.w3c_actions.key_action.pause = lambda *a, **k: None


class AlertBaseComponent:
    """
    Purpose:
    The base class for the component. A component is an UI component with which a user interacts with.
    The component class will have all the interaction method which can be done to the component.
    Implementation:
    - The component will have set of locators. Locators can be of type (ID, CSS_Selector, classname, Name, etc. whichever supported by selenium)
    - Each method will interact with theses locators directly.
    - The component should have a container, so that it does not have multiple confusing instances in a same page.
    - In a container, there should be only one component of the same type.
    """

    def __init__(self, browser, container):
        """
        :param browser: The instance of the selenium webdriver
        :param container: The container in which the component is located at.
        """
        self.elements = dict()
        self.browser = browser
        self.wait = WebDriverWait(self.browser, DEFAULT_TIMEOUT)
        self.elements["container"] = container

    def get_clear_text(self, web_element):
        """
        Gets the text of the web element
            :param web_element: The instance of the web element we are getting tect from.
            :returns: str the text of the web elements
        """
        return re.sub(r"\s+", " ", web_element.text).strip()

    def get_element(self, key):
        """
        Get the web-element.
        Note: There is a wait in get_element.
            :param key: The key of the element mentioned in self.elements
            :returns: element The element we are looking for by key
        """
        element = self.elements[key]
        return self._get_element(element.by, element.select)

    def get_elements(self, key):
        """
        Get the list of web-elements.
        Note: There is a wait in the method.
            :param key: The key of the element mentioned in self.elements
            :returns: list of elements we are searching for by key, or an empty list
        """
        try:
            self.wait_for(key)
            element = self.elements[key]
            return self._get_elements(element.by, element.select)
        except:
            return list()

    def get_child_element(self, key):
        """
        Get the web-element located inside the container.
            - It is more preferable to use get_child_element over get_element.
            - get_element should only be used if the element is out of the container for some reason. For example, in case of some pop-up.
        Note: There is a wait in the method.
            :param key: The key of the element mentioned in self.elements
            :returns: The child element of the element searched by key
        """
        element = self.elements[key]
        return self._get_child_element(element.by, element.select)

    def get_child_elements(self, key):
        """
        Get the list of web-elements located inside the container. Returns empty list of no elements found.
            - It is more preferable to use get_child_elements over get_elements.
            - get_elements should only be used if the element is out of the container for some reason. For example, in case of some pop-up.
        Note: There is a wait in the method.
            :param key: The key of the element mentioned in self.elements
            :returns: list The child elements of the element searched by key
        """
        try:
            self.wait_for(key)
            element = self.elements[key]
            return self._get_child_elements(element.by, element.select)
        except:
            return list()

    def get_tuple(self, key):
        """
        get the locator of the element in a tuple form.
            :param key: The key of the element mentioned in self.elements
            :returns: Tuple of the locator
        """
        return self.elements[key].by, self.elements[key].select

    def wait_for(self, key, msg=None, timeout=None):
        """
        if key in element, Wait for an web element to be visible. Raises TimeoutException if the element not found.
        if key is a condition, wait for the condition to be true.
            :param key: The key of the element mentioned in self.elements
            :param msg: The error-msg which should be mentioned in the TimeoutException
            :param timeout: The amount of time specified to wait for the wait function
        """
        if timeout:
            wait = WebDriverWait(self.browser, timeout)
        else:
            wait = self.wait
        if key in self.elements:
            if not msg:
                msg = "{} element is not present".format(key)
            return wait.until(EC.presence_of_element_located(self.get_tuple(key)), msg)
        else:
            if not msg:
                msg = "{}: Timeout while waiting for the condition to be true".format(
                    key
                )
            return wait.until(key, msg)

    def wait_for_text(self, key, msg=None):
        """
        if key in element, Wait for an text in web element to be visible. Raises TimeoutException if the text not element found.
            :param key: The key of the element mentioned in self.elements
            :param msg: The error-msg which should be mentioned in the TimeoutException
        """
        if not msg:
            msg = "Text not present in element {}".format(key)

        def _wait_for_text(browser):
            return len(self.get_element(key).text.strip()) > 0

        return self.wait_for(_wait_for_text, msg)

    def wait_until(self, key, msg=None):
        """
        Wait for an web element to be invisible. Raises TimeoutException if the element does not dissapear.
            :param key: The key of the element mentioned in self.elements
            :param msg: The error-msg which should be mentioned in the TimeoutException
        """
        if not msg:
            msg = "{} element did not disappear".format(key)
        self.wait.until(EC.invisibility_of_element_located(self.get_tuple(key)), msg)

    def wait_to_display(self):
        """
        Wait for the component container to be displayed
        """
        self.wait_for("container")

    def wait_to_be_stale(self, key, msg=None):
        if not msg:
            msg = "{} element is not stale.".format(key)
        wait = WebDriverWait(self.browser, DEFAULT_TIMEOUT)
        try:
            wait.until(EC.staleness_of(key), msg)
            return True
        except TimeoutException:
            pass

    def wait_to_be_clickable(self, key, msg=None):
        """
        Wait for an web element to be invisible. Raises TimeoutException if the element does not dissapear.
            :param key: The key of the element mentioned in self.elements
            :param msg: The error-msg which should be mentioned in the TimeoutException
        """
        if not msg:
            msg = "{} element is not clickable".format(key)
        self.wait.until(EC.element_to_be_clickable(self.get_tuple(key)), msg)

    def __getattr__(self, key):
        """
        Makes the web-elements to be accessible directly.
        - For example self.elements = {"textbox": Selector(by=..., select=...),
            Access the element by doing self.textbox directly.
        - It also has implicit wait while finding the element.
          :param key: The key of the element mentioned in self.elements
          :returns: The webelement we are accessing
        """
        try:
            return self.get_element(key)
        except KeyError:
            raise

    def hover_over_element(self, key):
        """
        Hover over an element, such as a tooltip, such that other items will appear
            :param key: The key of the element mentioned in self.elements
        """
        hover = (
            ActionChains(self.browser).move_to_element(self.get_element(key)).perform()
        )

    def _get_element(self, by, select):
        """
        Find the element from the page.
            :param by: The type of the selenium locator
            :param select: The selector text of type mentioned in by.
            :returns: The webelement we are accessing
        """
        msg = "by={} select={} Element not found in the page".format(by, select)
        return self.wait.until(EC.presence_of_element_located((by, select)), msg)

    def _get_elements(self, by, select):
        """
        Find the list of elements from the page.
            :param by: The type of the selenium locator
            :param select: The selector text of type mentioned in by.
            :returns: List of elements from the page
        """
        return self.browser.find_elements(by, select)

    def _get_child_element(self, by, select):
        """
        Find the element from the container.
            :param by: The type of the selenium locator
            :param select: The selector text of type mentioned in by.
            :returns: child element from the container
        """
        return self.container.find_element(by, select)

    def _get_child_elements(self, by, select):
        """
        Find the list of elements from the container.
            :param by: The type of the selenium locator
            :param select: The selector text of type mentioned in by.
            :returns: List of child elements from the page
        """
        return self.container.find_elements(by, select)


Selector = namedtuple("Selector", ["by", "select"], defaults=[By.CSS_SELECTOR, None])
