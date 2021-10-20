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

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from ..base_component import Selector
from .base_control import BaseControl


class Toggle(BaseControl):
    """
    Entity_Component : Button
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        """
        super().__init__(browser, container)
        self.elements.update(
            {
                "toggle_btn": Selector(
                    select=container.select
                    + ' [data-test="option"] [data-test="label"]'
                ),
                "selected": Selector(
                    select=container.select
                    + ' [data-test="option"][aria-checked="true"] [data-test="label"]'
                ),
            }
        )
        self.browser = browser
        self.container = container

    def select(self, value):
        """
        Selects the toggle specified
            :param value: the value to select
            :return: Bool if successful in selection, else raises an error
        """
        for each in self.get_elements("toggle_btn"):
            if each.text.lower() == value.lower():
                self._wait_to_be_clickable(each)
                return True
        else:
            raise ValueError("{} not found".format(value))

    def _wait_to_be_clickable(self, element):
        def try_click(self):
            try:
                element.click()
                return True
            except:
                return False

        WebDriverWait(self.browser, 10).until(try_click)

    def get_value(self):
        """
        Returns the value of the toggle element
            :return: Str the text for the toggle element
        """
        return self.selected.text.strip()
