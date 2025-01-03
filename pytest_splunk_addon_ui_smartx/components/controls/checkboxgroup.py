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
from selenium.webdriver.common.by import By

from ..base_component import Selector
from .base_control import BaseControl
from .checkbox import Checkbox
from .textbox import TextBox


class CheckboxGroup(BaseControl):
    """
    Entity_Component : CheckboxGroup

    This class represents a group of checkboxes, allowing for expanding groups,
    selecting/deselecting checkboxes, and setting or retrieving values.
    Note: Please use xpath as locator for this component.
    """

    def __init__(self, browser, container) -> None:
        """
        Initializes the CheckboxGroup.

        Args:
            browser (Browser): The browser instance to interact with.
            container (Selector): The container element that holds the checkbox group.
        """
        super().__init__(browser, container)

    def is_group_expanded(self, checkbox_group_name: str) -> bool:
        """
        Checks if the specified group is expanded.

        Args:
            checkbox_group_name (str): The name of the checkbox group to check.

        Returns:
            bool: True if the group is expanded, False otherwise.
        """
        self.elements.update(
            {
                f"{checkbox_group_name}_button": Selector(
                    by=By.XPATH,
                    select=self.elements.get("container").select
                    + f'//span[text()="{checkbox_group_name}"]/ancestor::button',
                )
            }
        )
        return (
            getattr(self, f"{checkbox_group_name}_button").get_attribute(
                "aria-expanded"
            )
            == "true"
        )

    def get_checkbox(self, checkbox_name: str) -> Checkbox:
        return Checkbox(
            self.browser,
            Selector(
                by=By.XPATH,
                select=self.elements.get("container").select
                + f"//div[@data-test-field='{checkbox_name}']/parent::div",
            ),
        )

    def select_checkbox_and_set_value(
        self, checkbox_group_name: str, checkbox_name: str, checkbox_value: str = None
    ) -> None:
        """
        Expands a group and selects a checkbox, then sets the specified value.

        Args:
            checkbox_group_name (str): The name of the group to expand.
            checkbox_name (str): The name of the checkbox to select.
            checkbox_value (str): The value to set for the checkbox.
        """
        self.expand_group(checkbox_group_name)
        self.get_checkbox(checkbox_name).check()
        if checkbox_value:
            self.get_textbox(checkbox_name).set_value(checkbox_value)

    def deselect(self, checkbox_group_name: str, checkbox_name: str) -> None:
        """
        Expands a group and deselects the specified checkbox.

        Args:
            checkbox_group_name (str): The name of the group to expand.
            checkbox_name (str): The name of the checkbox to deselect.
        """
        self.expand_group(checkbox_group_name)
        self.get_checkbox(checkbox_name).uncheck()

    def get_textbox(self, checkbox_name: str) -> TextBox:
        return TextBox(
            self.browser,
            Selector(
                by=By.XPATH,
                select=self.elements.get("container").select
                + f"//div[@data-test-field='{checkbox_name}' and @data-test='number']",
            ),
        )

    def get_checkbox_text_value(
        self, checkbox_group_name: str, checkbox_name: str
    ) -> str:
        """
        Expands a group and retrieves the text value of the specified checkbox.

        Args:
            checkbox_group_name (str): The name of the group to expand.
            checkbox_name (str): The name of the checkbox to retrieve the value from.

        Returns:
            str: The value of the checkbox.
        """
        self.expand_group(checkbox_group_name)
        return self.get_textbox(checkbox_name).get_value()

    def expand_group(self, checkbox_group_name: str) -> None:
        """
        Expands the specified group if it is not already expanded.

        Args:
            checkbox_group_name (str): The name of the group to expand.
        """
        is_expanded = self.is_group_expanded(checkbox_group_name)
        if not is_expanded:
            getattr(self, f"{checkbox_group_name}_button").click()

    def collapse_group(self, checkbox_group_name: str) -> None:
        """
        collapse the specified group if it is not already expanded.

        Args:
            checkbox_group_name (str): The name of the group to expand.
        """
        is_expanded = self.is_group_expanded(checkbox_group_name)
        if is_expanded:
            getattr(self, f"{checkbox_group_name}_button").click()
