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

from ..base_component import Selector
from .base_control import BaseControl


class OAuthSelect(BaseControl):
    """
    Entity-Component: Select

    OAuthSelect Javascript framework: OAuthSelect

    A dropdown which can select only one value
    """

    def __init__(self, browser, container, searchable=True):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        """

        super().__init__(browser, container)
        self.elements.update(
            {
                "root": Selector(select=container.select + ' [data-test="select"]'),
                "values": Selector(select=container.select + ' [data-test="option"]'),
            }
        )

    def select(self, value):
        """
        Selects the value within hte select dropdown
            :param value: the value to select
            :return: Bool if successful in selection, else raises an error
        """

        self.root.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {
                "values": Selector(
                    select=popover_id
                    + ' [data-test="option"]:not([data-test-selected="true"]) [data-test="label"]'
                )
            }
        )
        for each in self.get_elements("values"):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def get_value(self):
        """
        Gets the selected value
            :return: Str The elected value within the dropdown, else returns blank
        """
        try:
            return self.root.get_attribute("data-test-value")
        except:
            return ""

    def list_of_values(self):
        """
        Gets the list of value from the Single Select
            :returns: List of options from the single select
        """
        selected_val = self.get_value()
        self.root.click()
        first_element = None
        list_of_values = []
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {"values": Selector(select=popover_id + ' [data-test="option"]')}
        )
        for each in self.get_elements("values"):
            list_of_values.append(each.text.strip())
        return list_of_values
