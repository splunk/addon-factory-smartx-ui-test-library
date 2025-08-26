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

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from ..base_component import Selector
from .base_control import BaseControl


class SingleSelect(BaseControl):
    """
    Entity-Component: Select, ComboBox

    A dropdown which can select only one value
    """

    def __init__(self, browser, container, searchable=True, allow_new_values=False):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        :param searchable: Boolean indicating if the dropdown provides filter or not.
        :param allow_new_values: Boolean indicating if the dropdown allows for user-entered custom values
         excluding a predefined list.
        """
        super().__init__(browser, container)
        self.searchable = searchable
        # Component is ComboBox in case of True
        self.allow_new_values = allow_new_values
        self.container = container

        if not self.searchable and self.allow_new_values:
            raise ValueError(
                "Invalid combination of values for searchable and allow_new_values flags"
            )

        self.element_selector = container.select + (
            ' [data-test="combo-box"]' if allow_new_values else ' [data-test="select"]'
        )

        self.elements.update(
            {
                "root": Selector(select=self.element_selector),
                "selected": Selector(
                    select=container.select + ' [data-test="textbox"]'
                ),
                "cancel_selected": Selector(
                    select=container.select + ' [data-test="clear"]'
                ),
            }
        )

    def select(self, value, open_dropdown=True):
        """
        Selects the value within the select dropdown
            :param value: the value to select
            :param open_dropdown: Whether the dropdown should be opened
            :return: Bool if successful in selection, else raises an error
        """
        if open_dropdown:
            self.wait_to_be_clickable("root")
            self.root.click()

        if self.allow_new_values and self.get_value():
            self.wait_to_be_clickable("cancel_selected")
            self.cancel_selected.click()

        popover_id = "#" + self.root.get_attribute("data-test-popover-id")

        self.elements.update(
            {
                "values": Selector(select=popover_id + ' [data-test="option"]'),
                "dropdown": Selector(select=popover_id + ' [data-test="menu"]'),
                "combobox": Selector(select=popover_id + ' [data-test="menu"]'),
            }
        )

        for each in self.get_elements("values"):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def search(self, value, open_dropdown=True):
        """
        search with the singleselect input
            :param value: string value to search
            :assert Asserts whether the single select is searchable
        """
        assert self.searchable, "Can not search, as the Singleselect is not searchable"
        if open_dropdown:
            self.wait_to_be_clickable("root")
            self.root.click()
        if self.searchable:
            if self.allow_new_values:
                self.elements.update(
                    {
                        "input": Selector(
                            select=self.element_selector + ' [data-test="textbox"]'
                        )
                    }
                )
            else:
                popover_id = "#" + self.root.get_attribute("data-test-popover-id")
                self.elements.update(
                    {"input": Selector(select=popover_id + ' [data-test="textbox"]')}
                )

        self.input.send_keys(value)
        # DEBUG: maybe we have to click the select button

    def search_get_list(self, value):
        """
        search with the singleselect input and return the list
            :param value: string value to search
            :return: a list of values
        """

        if self.searchable:
            if self.allow_new_values:
                self.elements.update(
                    {
                        "input": Selector(
                            select=self.element_selector + ' [data-test="textbox"]'
                        )
                    }
                )
            else:
                self.wait_to_be_clickable("root")
                self.root.click()
                popover_id = "#" + self.root.get_attribute("data-test-popover-id")
                self.elements.update(
                    {"input": Selector(select=popover_id + ' [data-test="textbox"]')}
                )
        # as the dropdown is already open we dont try to open it
        self.search(value, open_dropdown=False)
        if self.allow_new_values:
            searched_values = list(self._list_visible_values())
        else:
            self.wait_for_search_list()
            searched_values = list(self._list_visible_values(open_dropdown=False))
            self.input.send_keys(Keys.ESCAPE)
            self.wait_for("root")

        return searched_values

    def _list_visible_values(self, open_dropdown=True):
        """
        Gets a list of values which are visible. Used while filtering
            :param open_dropdown: Whether the dropdown should be opened
            :return: List of the values that are visible
        """
        if open_dropdown:
            self.wait_to_be_clickable("root")
            self.root.click()

        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        if self.allow_new_values:
            self.elements.update(
                {"values": Selector(select=popover_id + ' [data-test="option"]')}
            )
        else:
            self.elements.update(
                {
                    "values": Selector(
                        select=popover_id
                        + ' [data-test="option"]:not([data-test-selected="true"]) [data-test="label"]'
                    )
                }
            )
        for each in self.get_elements("values"):
            yield each.get_attribute(
                "data-test-current-value-option"
            ) or each.get_attribute("textContent")

    def get_value(self):
        """
        Gets the selected value
            :return: The selected value's text, or returns false if unsuccessful
        """
        if self.allow_new_values:
            # ComboBox do not support label
            return self.selected.get_attribute("value")
        else:
            if self.root.get_attribute(
                "data-test-loading"
            ) == "false" and self.root.get_attribute("data-test-value"):
                nested_span_element = self.root.find_element(
                    By.CSS_SELECTOR, "span > span"
                )
                if nested_span_element:
                    return nested_span_element.text
                return self.root.get_attribute("label")
            else:
                return False

    def cancel_selected_value(self):
        """
        Cancels the currently selected value in the SingleSelect
            :return: Bool whether canceling the selected item was successful, else raises an error
        """
        self.wait_to_be_clickable("root")
        self.root.click()
        self.wait_to_be_clickable("cancel_selected")
        self.cancel_selected.click()
        return True

    def list_of_values(self):
        """
        Gets the list of value from the Single Select
            :return: list of options avaialble within the single select
        """
        selected_val = self.get_value()
        self.wait_to_be_clickable("root")
        self.root.click()
        first_element = None
        list_of_values = []

        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        if self.allow_new_values:
            if self.searchable:
                self.elements.update(
                    {
                        "input": Selector(
                            select=self.container.select + ' [data-test="textbox"]'
                        )
                    }
                )
        else:
            if self.searchable:
                self.elements.update(
                    {"input": Selector(select=popover_id + ' [data-test="textbox"]')}
                )
        self.elements.update(
            {"values": Selector(select=popover_id + ' [data-test="option"]')}
        )

        for each in self.get_elements("values"):
            if not first_element:
                first_element = each
            list_of_values.append(each.text.strip())
        if selected_val and not self.allow_new_values:
            # as the dropdown is already open we dont try to open it
            self.select(selected_val, open_dropdown=False)
        elif self.searchable:
            self.input.send_keys(Keys.ESCAPE)
        elif first_element:
            self.select(first_element.text.strip(), open_dropdown=False)
        self.wait_for("root")
        return list_of_values

    def get_single_value(self):
        """
        :return: one value from Single Select
        """
        selected_val = self.get_value()

        self.wait_to_be_clickable("root")
        self.root.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        if self.allow_new_values:
            if self.searchable:
                self.elements.update(
                    {
                        "input": Selector(
                            select=self.container.select + ' [data-test="textbox"]'
                        )
                    }
                )
            self.elements.update(
                {
                    "values": Selector(
                        select=popover_id
                        + ' [data-test="option"]:not([data-test-selected="true"]) [data-test="label"]'
                    )
                }
            )
        else:
            if self.searchable:
                self.elements.update(
                    {"input": Selector(select=popover_id + ' [data-test="textbox"]')}
                )
            self.elements.update(
                {"values": Selector(select=popover_id + ' [data-test="option"]')}
            )

        single_element = self.get_element("values")

        if selected_val and not self.allow_new_values:
            # as the dropdown is already open, we don't try to open it
            self.select(selected_val, open_dropdown=False)
        elif self.searchable:
            self.input.send_keys(Keys.ESCAPE)
        else:
            self.select(single_element.text.strip(), open_dropdown=False)
        self.wait_for("root")
        return single_element

    def get_list_count(self):
        """
        Gets the total count of the SingleSelect list
            :return: Int the count of the options within the Single Select
        """
        return len(list(self.list_of_values()))

    def wait_for_values(self):
        """
        Wait for dynamic values to load in SingleSelect
        """

        def _wait_for_values(driver):
            return self.get_single_value()

        self.wait_for(_wait_for_values, msg="No values found in SingleSelect")

    def wait_for_search_list(self):
        """
        Wait for SingleSelect search to populate
        """

        def _wait_for_search_list(driver):
            return len(list(self._list_visible_values(open_dropdown=False))) > 0

        self.wait_for(
            _wait_for_search_list, msg="No values found in SingleSelect search"
        )

    def allow_new_values(self) -> bool:
        """
        Returns True if the SingleSelect accepts new values, False otherwise
        """
        self.get_element("root")
        return True if self.allow_new_values else False

    def is_editable(self) -> bool:
        """
        Returns True if the SingleSelect is editable, False otherwise
        """
        if self.allow_new_values:
            return (
                not self.selected.get_attribute("readonly")
                and not self.selected.get_attribute("readOnly")
                and not self.selected.get_attribute("disabled")
            )
        else:
            return (
                not self.root.get_attribute("readonly")
                and not self.root.get_attribute("readOnly")
                and not self.root.get_attribute("disabled")
            )
