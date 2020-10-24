# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from .base_control import BaseControl
from selenium.webdriver.common.by import By
import time

class LearnMore(BaseControl):
    """
    Entity_Component : Learn More
    """
    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in. 
        """
        super(LearnMore, self).__init__(browser, container)

    def go_to_link(self):
        '''
        Redirects the browser object to the link provided by the container and returns the URL
        '''
        self.container.click()
        self.wait_for_tab()
        # For Safari window_handles works opposite as compared to Firefox and Chrome 
        # In Safari window_handles[1] represents the current window.
        # And in other browsers window_handels[0] represents the current window.
        if self.browser.name == "Safari":
            self.browser.switch_to.window(self.browser.window_handles[0])
        else:
            self.browser.switch_to.window(self.browser.window_handles[1])
        self.wait_for_header()
        current_url = self.browser.current_url
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        return current_url

    def wait_for_tab(self):
        """
        Wait for redirect page title to load.
        """
        def _wait_for_tab(driver):
            return len(self.browser.window_handles) > 1
        self.wait_for(_wait_for_tab, msg="Redirect page didn't open")

    def wait_for_header(self):
        """
        Wait for header 
        """
        def _wait_for_header(driver):
            return driver.find_element_by_tag_name("header")
        self.wait_for(_wait_for_header, msg="Redirect page didn't open")