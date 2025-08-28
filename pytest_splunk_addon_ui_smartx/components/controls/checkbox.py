#
# Copyright 2025 Splunk Inc.
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
        if container.by == "xpath":
            self.elements.update(
                {
                    "internal_container": Selector(
                        by=By.XPATH,
                        select=container.select + '//div[@data-test="switch"]',
                    ),
                    "checkbox": Selector(
                        by=By.XPATH,
                        select=container.select + '//div[@data-test="switch"]',
                    ),
                    "checkbox_btn": Selector(
                        by=By.XPATH,
                        select=container.select + '//button[@role="checkbox"]',
                    ),
                }
            )
        else:
            self.elements.update(
                {
                    "internal_container": Selector(
                        select=container.select + ' [data-test="switch"]'
                    ),
                    "checkbox": Selector(
                        select=container.select + ' [data-test="switch"]'
                    ),
                    "checkbox_btn": Selector(
                        select=container.select
                        + ' div[data-test="controls"] button[role="checkbox"]'
                    ),
                }
            )

    def toggle(self, max_attempts=5):
        """
        Toggles the checkbox value
        """
        before_toggle = self.is_checked()
        for _ in range(max_attempts):
            try:
                self.wait_to_be_clickable("checkbox")
                self.checkbox_btn.click()
                after_toggle = self.is_checked()
                if before_toggle != after_toggle:
                    return
                time.sleep(0.25)
            except Exception as e:
                print(f"Toggle checkbox failed with {e}")

    def check(self):
        """
        Checks the checkbox if unchecked
            :return: Bool true if successful, else it will return a statement that it was already checked
        """
        try:
            if self.is_checked() == False:
                self.toggle()
                return True
            else:
                return "Checkbox is already checked"
        except Exception as e:
            print(f"Check checkbox failed with {e}")

    def uncheck(self):
        """
        Unchecks the checkbox if checked
            :return: Bool true if successful, else it will return a statement that it was already unchecked
        """
        try:
            if self.is_checked() == True:
                self.toggle()
                return True
            else:
                return "Checkbox is already unchecked"
        except Exception as e:
            print(f"Uncheck checkbox failed with {e}")

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
