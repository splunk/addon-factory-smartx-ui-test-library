#
# Copyright 2024 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time
from contextlib import contextmanager

from selenium.webdriver.common.by import By

from ..base_component import Selector
from .base_control import BaseControl


class LearnMore(BaseControl):
    """
    Entity_Component : Learn More
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        """
        super().__init__(browser, container)
        self.elements.update(
            {
                "internal_container": Selector(
                    select=container.select + ' [data-test="link"]'
                ),
            }
        )

    @contextmanager
    def open_link(self, open_new_tab=True):
        """
        Redirects the browser object to the link provided by the container and returns the URL
        """
        page_url = self.browser.current_url
        self.internal_container.click()
        # For Safari window_handles works opposite as compared to Firefox and Chrome
        # In Safari window_handles[1] represents the current window.
        # And in other browsers window_handels[0] represents the current window.
        if open_new_tab:
            self.wait_for_tab()
            if self.browser.name == "Safari":
                self.browser.switch_to.window(self.browser.window_handles[0])
            else:
                self.browser.switch_to.window(self.browser.window_handles[1])

            current_url = self.browser.current_url
            yield current_url
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
        else:
            self.wait_for_url_change(page_url)
            current_url = self.browser.current_url
            yield current_url

    def get_current_url(self):
        return self.browser.current_url

    def wait_for_tab(self):
        """
        Wait for redirect page title to load.
        """

        def _wait_for_tab(driver):
            return len(self.browser.window_handles) > 1

        self.wait_for(_wait_for_tab, msg="Redirect page didn't open")

    def wait_for_url_change(self, page_url):
        """
        Wait for url to be change
        """

        def _wait_for_url_change(driver):
            return self.browser.current_url != page_url

        self.wait_for(_wait_for_url_change, msg="Redirect page didn't open")
