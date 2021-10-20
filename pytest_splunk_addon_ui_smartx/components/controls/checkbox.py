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

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ..base_component import Selector
from .base_control import BaseControl


class Checkbox(BaseControl):
    """
    Entity_Component : Checkbox
    """

    def __init__(self, browser, container, searchable=True):
        super().__init__(browser, container)
        self.elements.update(
            {
                "internal_container": Selector(
                    select=container.select + ' [data-test="switch"]'
                ),
                "checkbox": Selector(select=container.select + ' [data-test="switch"]'),
                "checkbox_btn": Selector(
                    select=container.select + ' [data-test="button"][role="checkbox"]'
                ),
            }
        )

    def toggle(self):
        """
        Toggles the checkbox value
        """
        self.wait_to_be_clickable("checkbox")
        self.checkbox_btn.click()

    def check(self):
        """
        Checks the checkbox if unchecked
            :return: Bool true if successful, else it will return a statement that it was already checked
        """
        try:
            if self.is_checked() == False:
                self.toggle()
            return True
        except:
            return "Checkbox is already checked"

    def uncheck(self):
        """
        Unchecks the checkbox if checked
            :return: Bool true if successful, else it will return a statement that it was already unchecked
        """
        try:
            if self.is_checked() == True:
                self.toggle()
            return True
        except:
            return "Checkbox is already unchecked"

    def is_checked(self):
        """
        Returns True if the checkbox is already checked, otherwise False
            :return: Bool True if checked, False if unchecked
        """
        is_selected = self.checkbox.get_attribute("data-test-selected")
        if is_selected == "true":
            return True
        else:
            return False
