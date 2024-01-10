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

from selenium.webdriver.support.ui import Select

from .action_controls import ActionControls
from .alert_base_component import AlertBaseComponent, Selector
from .alert_base_control import AlertBaseControl


class AlertSingleSelect(ActionControls):
    def __init__(self, browser, container):
        super().__init__(browser, container)
        self.elements.update(
            {
                "internal_container": Selector(select=container.select),
            }
        )

    def select(self, value, open_dropdown=True):
        select_obj = Select(self.internal_container)
        select_obj.select_by_visible_text(value)
        return True

    def get_value(self):
        """
        Gets the selected value
        """
        select_obj = Select(self.internal_container)
        return self.get_clear_text(select_obj.first_selected_option)

    def list_of_values(self):
        """
        Gets the list of value from the Single Select
        """
        select_obj = Select(self.internal_container)
        value_list = []
        for each_obj in select_obj.options:
            value_list.append(self.get_clear_text(each_obj))

        return value_list
