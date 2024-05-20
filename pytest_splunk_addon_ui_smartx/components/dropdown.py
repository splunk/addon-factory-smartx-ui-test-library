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
from .base_component import BaseComponent, Selector
from selenium.common.exceptions import ElementClickInterceptedException


class Dropdown(BaseComponent):
    """
    Component: Dropdown
    Base class of Input & Configuration table
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
        """
        super().__init__(browser, container)
        self.elements.update(
            {
                "root": Selector(select=container.select),
                "currunt_value": Selector(
                    select=container.select
                    + ' [data-test="select"] [data-test="label"]'
                ),
                "type_dropdown": Selector(select=container.select),
            }
        )

    def select_page_option(self, value):
        """
        Selects the page option that the user specifies in value
            :param value: The value in which we want to select
            :return: Returns True if successful, otherwise raises an error
        """
        self.wait_to_be_clickable("root")
        self.root.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {
                "page_list": Selector(select=popover_id + ' [data-test="label"]'),
            }
        )
        for each in self.get_elements("page_list"):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def get_value(self):
        """
        Returns the current value for the dropdown
            :return: Str The current value for the dropdown
        """
        return self.currunt_value.text.strip()

    def select(self, value):
        """
        Selects the value we want from the type list
            :param value: The value in which we want to select
            :return: Returns True if successful, otherwise raises an error
        """
        self.wait_to_be_clickable("root")
        self.root.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {
                "pagination_dropdown": Selector(
                    select=popover_id + '[data-test="menu"]'
                ),
                "values": Selector(
                    select=popover_id
                    + ' [data-test="item"]:not([data-test-selected="true"]) [data-test="label"]'
                ),
            }
        )

        for each in self.get_elements("values"):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def select_nested(self, values: list):
        """
        Selects the values we want from the type list in defined order
            :param values: Dropdown values list in order we want to select
            :return: Returns True if successful, otherwise raises an error
        """
        if not isinstance(values, list):
            raise ValueError("{} has to be of type list".format(values))
        self.wait_to_be_clickable("root")
        self.root.click()
        popoverid = "#" + self.root.get_attribute("data-test-popover-id")
        dropdown_selector = ' [data-test="item"] [data-test="label"]'
        for value in values:
            found = False
            self.elements.update(
                {"dropdown_options": Selector(select=popoverid + dropdown_selector)}
            )
            for each in self.get_elements("dropdown_options"):
                if each.text.strip().lower() == value.lower():
                    found = True
                    try:
                        each.click()
                    except ElementClickInterceptedException:
                        self.hover_over_element("root")  # avoid tooltip interception
                        each.click()
                    time.sleep(
                        1
                    )  # sleep here prevents broken animation resulting in unclicable button
                    break
            if not found:
                raise ValueError(
                    f"{value} not found in select list. Values found {[_.text.strip().lower() for _ in self.get_elements('dropdown_options')]}"
                )
        return True

    def select_input_type(self, value, open_dropdown=True):
        """
        Selects the input type option that the user specifies in value
            :param value: The value in which we want to select
            :param open_dropdown: Whether the dropdown should be opened
            :return: Returns True if successful, otherwise raises an error
        """
        if open_dropdown:
            self.wait_to_be_clickable("root")
            self.root.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {
                "type_filter_list": Selector(
                    select=popover_id + ' [data-test="label"]'
                ),
            }
        )
        for each in self.get_elements("type_filter_list"):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def get_inputs_list(self):
        """
        Returns a generator list for the options available in the add input dropdown
            :return: Returns Generator list of values
        """
        self.wait_to_be_clickable("root")
        self.root.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {
                "type_list": Selector(select=popover_id + ' [data-test="item"]'),
            }
        )
        return [each.text.strip() for each in self.get_elements("type_list")]

    def get_pagination_list(self):
        """
        Returns a generator list for the pagination text available in the add input dropdown
            :return: Returns Generator list of values
        """
        self.wait_to_be_clickable("root")
        self.root.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {
                "page_list": Selector(select=popover_id + ' [data-test="label"]'),
            }
        )
        return [each.text.strip() for each in self.get_elements("page_list")]

    def get_input_type_list(self):
        """
        Returns a generator list for the input types available in the add input dropdown
            :return: Returns Generator list of values
        """
        self.wait_to_be_clickable("root")
        self.root.click()
        popover_id = "#" + self.root.get_attribute("data-test-popover-id")
        self.elements.update(
            {
                "type_filter_list": Selector(
                    select=popover_id + ' [data-test="label"]'
                ),
            }
        )
        return [each.text.strip() for each in self.get_elements("type_filter_list")]

    def wait_to_be_stale(self, msg=None):
        return super().wait_to_be_stale(key=self.get_element("root"), msg=msg)
