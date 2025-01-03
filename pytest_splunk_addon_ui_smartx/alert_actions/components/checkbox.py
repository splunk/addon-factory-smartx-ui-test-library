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
from .action_controls import ActionControls
from .alert_base_component import Selector
from .alert_base_control import AlertBaseControl


class AlertCheckbox(ActionControls):
    def __init__(self, browser, container):
        super().__init__(browser, container)
        self.elements.update(
            {
                "internal_container": Selector(
                    select=container.select + " div.select2-container"
                ),
                "checkbox": Selector(select=container.select),
                "checkbox_btn": Selector(select=container.select + " .checkbox a.btn"),
                "checkbox_enabled": Selector(
                    select=container.select + " .checkbox a.btn .icon-check"
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
                self.checkbox.click()
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
        return self.checkbox.is_selected()
