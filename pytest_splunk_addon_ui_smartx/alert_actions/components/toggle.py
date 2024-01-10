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

from .action_controls import ActionControls
from .alert_base_component import Selector
from .alert_base_control import AlertBaseControl


class AlertToggle(ActionControls):
    def __init__(self, browser, container):
        super().__init__(browser, container)
        self.elements.update(
            {
                "toggle_btn": Selector(select=container.select),
                "selected": Selector(select=container.select + " .active"),
            }
        )

    def select(self, value):
        """
        Selects the toggle specified
            :param value: the value to select
            :return: Bool if successful in selection, else raises an error
        """
        for each in self.get_elements("toggle_btn"):
            if each.get_attribute("value").strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found".format(value))

    def get_value(self):
        for each in self.get_elements("toggle_btn"):
            if each.is_selected():
                return each.get_attribute("value")
