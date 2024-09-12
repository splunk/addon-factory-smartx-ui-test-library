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
from selenium.webdriver.common.by import By

from ..base_component import Selector
from .base_control import BaseControl
from .button import Button
from .checkbox import Checkbox
from .textbox import TextBox

class CheckboxGroup(BaseControl):
    """
    Entity_Component : CheckboxGroup

    This class represents a group of checkboxes, allowing for expanding groups,
    selecting/deselecting checkboxes, and setting or retrieving values.
    """

    def __init__(self, browser, container) -> None:
        """
        Initializes the CheckboxGroup.

        Args:
            browser (Browser): The browser instance to interact with.
            container (Selector): The container element that holds the checkbox group.
        """
        super().__init__(browser, container)

    def is_group_expanded(self, group_name: str) -> bool:
        """
        Checks if the specified group is expanded.

        Args:
            group_name (str): The name of the checkbox group to check.

        Returns:
            bool: True if the group is expanded, False otherwise.
        """
        self.elements.update({
            f"{group_name}_button": Selector(
                by=By.XPATH,
                select=self.elements.get("container").select + f'//span[text()="{group_name}"]/ancestor::button'
            )
        })
        return getattr(self, f"{group_name}_button").get_attribute("aria-expanded") == "true"

    def select_checkbox_and_set_value(self, checkbox_name: str, checkbox_value: str) -> None:
        """
        Selects a checkbox and sets a value for the checkbox.

        Args:
            checkbox_name (str): The name of the checkbox to select.
            checkbox_value (str): The value to set for the checkbox.
        """
        Checkbox(
            self.browser,
            Selector(
                by=By.XPATH,
                select=self.elements.get("container").select + f"//div[@data-test-field='{checkbox_name}']/parent::div"
            )
        ).check()
        TextBox(
            self.browser,
            Selector(
                by=By.XPATH,
                select=self.elements.get("container").select + f"//div[@data-test-field='{checkbox_name}' and @data-test='number']"
            )
        ).set_value(checkbox_value)

    def select(self, group_name: str, checkbox_name: str, checkbox_value: str) -> None:
        """
        Expands a group and selects a checkbox, then sets the specified value.

        Args:
            group_name (str): The name of the group to expand.
            checkbox_name (str): The name of the checkbox to select.
            checkbox_value (str): The value to set for the checkbox.
        """
        self.expand_group(group_name)
        self.select_checkbox_and_set_value(checkbox_name=checkbox_name, checkbox_value=checkbox_value)

    def deselect(self, group_name: str, checkbox_name: str) -> None:
        """
        Expands a group and deselects the specified checkbox.

        Args:
            group_name (str): The name of the group to expand.
            checkbox_name (str): The name of the checkbox to deselect.
        """
        self.expand_group(group_name)
        Checkbox(
            self.browser,
            Selector(
                by=By.XPATH,
                select=self.elements.get("container").select + f"//div[@data-test-field='{checkbox_name}']/parent::div"
            )
        ).uncheck()

    def get_checkbox_value(self, group_name: str, checkbox_name: str) -> str:
        """
        Expands a group and retrieves the value of the specified checkbox.

        Args:
            group_name (str): The name of the group to expand.
            checkbox_name (str): The name of the checkbox to retrieve the value from.

        Returns:
            str: The value of the checkbox.
        """
        self.expand_group(group_name)
        return TextBox(
            self.browser,
            Selector(
                by=By.XPATH,
                select=self.elements.get("container").select + f"//div[@data-test-field='{checkbox_name}' and @data-test='number']"
            )
        ).get_value()

    def expand_group(self, group_name: str) -> None:
        """
        Expands the specified group if it is not already expanded.

        Args:
            group_name (str): The name of the group to expand.
        """
        is_expanded = self.is_group_expanded(group_name)
        if not is_expanded:
            getattr(self, f"{group_name}_button").click()
