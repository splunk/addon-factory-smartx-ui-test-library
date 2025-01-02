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
from selenium.common.exceptions import TimeoutException


class File(BaseControl):
    """
    Entity-Component: File
    """

    def __init__(self, browser, container) -> None:
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        """
        super().__init__(browser, container)
        self.elements.update(
            {
                "input": Selector(select=container.select + " input"),
                "support_message": Selector(
                    select=container.select
                    + ' [data-test="file"] [data-test="file-supports"]'
                ),
                "error_text": Selector(
                    select=container.select + ' [data-test="file"] [data-test="help"]'
                ),
                "selected": Selector(
                    select=container.select + ' [data-test="item"] [data-test="label"]'
                ),
                "cancel_selected": Selector(
                    select=container.select + ' [data-test="remove"]'
                ),
            }
        )

    def set_value(self, value: str) -> None:
        """
        set value of the File input
        """
        self.wait_for("input")
        self.input.send_keys(value)

    def get_value(self) -> str:
        """
        get the name of the selected file
            :return: Str The name of the selected file
        """
        try:
            return self.selected.get_attribute("innerText").strip()
        except TimeoutException:
            pass
        return ""

    def get_support_message(self) -> str:
        """
        get the file support message
            :return: Str file support message
        """
        return self.support_message.get_attribute("innerText").strip()

    def get_error_text(self) -> str:
        """
        get the file validation error text
            :return: Str error message of the file validation
        """
        try:
            return self.error_text.get_attribute("innerText").strip()
        except TimeoutException:
            pass
        return ""

    def cancel_selected_value(self) -> bool:
        """
        Cancels the currently selected value in the File component
            :return: Bool whether canceling the selected item was successful, else raises an error
        """
        self.wait_to_be_clickable("cancel_selected")
        self.cancel_selected.click()
        return True
