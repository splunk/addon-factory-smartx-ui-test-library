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

from selenium.common.exceptions import ElementClickInterceptedException

from selenium.webdriver.common.keys import Keys

from ..base_component import Selector
from .base_control import BaseControl


class MultiSelect(BaseControl):
    """
    Entity-Component: Multiselect
    A dropdown which can select more than one values
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in
        """
        super().__init__(browser, container)

        root_selector = container.select + ' [data-test="multiselect"]'
        self.elements.update({"root": Selector(select=root_selector)})

        self.elements.update(
            {
                "selected": Selector(
                    # changes w.r.t. splunk-ui 4.30.0
                    select=root_selector
                    + ' [data-test="selected-option"] div[data-test="label"]'
                ),
                """
                Click on selected element deselects it
                """
                "deselect": Selector(
                    # changes w.r.t. splunk-ui 4.30.0
                    select=root_selector
                    + ' [data-test="selected-option"] div[data-test="label"]'
                ),
                "input": Selector(select=root_selector + ' [data-test="textbox"]'),
            }
        )

    def search(self, value):
        """
        search with the multiselect input
            :param value: string value to search
        """
        self.input.send_keys(value)

    def clear_text(self):
        """
        Clears the search box value in the multiselect field
        """
        self.input.clear()

    def search_get_list(self, value):
        """
        search with the multiselect input and return the list
            :param value: string value to search
            :return: list of values
        """
        self.search(value)
        self.wait_for_search_list()
        searched_values = list(self._list_visible_values())
        self.input.send_keys(Keys.ESCAPE)
        return searched_values

    def select(self, value):
        """
        select a single value
            :param value: the value to select
            :return: Bool returns true if selection was successful, else raises an exception
        """
        try:
            try:
                self.input.click()
            except ElementClickInterceptedException:
                self.label_text.click()
                self.input.click()

        except:
            raise Exception("dropdown not found")

        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {"values": Selector(select=popover_id + ' [data-test="option"]')}
        )
        for each in self.get_elements("values"):
            if each.text.strip().lower() == value.lower():
                try:
                    each.click()
                except ElementClickInterceptedException:
                    self.elements.update(
                        {
                            value.lower(): Selector(
                                select=popover_id
                                + f' [data-test="option"][data-test-value="{value.lower()}"]'
                            )
                        }
                    )
                    self.hover_over_element(f"{value.lower()}")
                    each.click()
                self.wait_for("input")
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def deselect(self, value):
        """
        Remove an item from selected list.
            :param value: the value to deselect
            :return: Bool returns true if deselect was successful, else raises an exception
        """
        for each in self.get_child_elements("selected"):
            if each.text.strip().lower() == value.lower():
                each.click()
                self.wait_for("root")
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def deselect_all(self):
        """
        Remove all items from selected list.
        """
        for each in self.get_values():
            self.deselect(each)

    def get_values(self):
        """
        get list selected values
            :return: List of values selected within the multi-select
        """
        return [each.text.strip() for each in self.get_child_elements("selected")]

    def list_of_values(self):
        """
        Get list of possible values to select from dropdown
            :return: List of options within the multi-select dropdown
        """
        self.wait_for("root")
        list_of_values = []
        self.input.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {
                "values": Selector(
                    select=popover_id + ' [data-test="option"] [data-test="label"]'
                )
            }
        )
        for each in self.get_elements("values"):
            list_of_values.append(each.text.strip())
        return list_of_values

    def get_list_count(self):
        """
        Gets the total count of the Multiselect list
        """
        return len(list(self.list_of_values()))

    def _list_visible_values(self):
        """
        Get list of values which are visible. Used while filtering
            :return: List of visible options within the multi-select dropdown
        """
        self.input.click()
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
            yield each.get_attribute("textContent")

    def wait_for_values(self):
        """
        Wait for dynamic values to load in Mulitple select
        """

        def _wait_for_values(driver):
            return self.get_list_count() > 0

        self.wait_for(_wait_for_values, msg="No values found in Multiselect")

    def wait_for_search_list(self):
        """
        Wait for Multiselect search to populate
        """

        def _wait_for_search_list(driver):
            return len(list(self._list_visible_values())) > 0

        self.wait_for(
            _wait_for_search_list, msg="No values found in Multiselect search"
        )
