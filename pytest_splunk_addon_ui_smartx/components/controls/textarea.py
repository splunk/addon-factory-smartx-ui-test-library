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
import platform

from selenium.webdriver.common.keys import Keys

from ..base_component import Selector
from .textbox import TextBox

os_base = platform.system()


class TextArea(TextBox):
    """
    Entity-Component: TextBox
    """

    def __init__(self, browser, container, encrypted=False):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        """
        super().__init__(browser, container)
        self.elements.update(
            {
                "input": Selector(
                    select=container.select + ' textarea[data-test="textbox"]'
                )
            }
        )

    def get_value(self):
        """
        get value from the textbox
            :return: Str The current value of the textbox
        """
        return self.input.get_attribute("value")

    def get_textarea_height(self) -> int:
        """
        Get the height of the displayed textarea.
            :return: Int Height of the textarea in pixels.
        """
        return self.input.size["height"]

    def append_value(self, value) -> None:
        """
        Appends the specified 'value' to an textarea element
        """
        self.input.send_keys(value)

    def screenshot(self) -> str:
        """
        Creates screenshot of current element
            :return: screenshot as base64
        """
        return self.input.screenshot_as_base64

    def scroll(self, direction: str, scroll_count: int) -> None:
        """
        Scrolls the input element in the specified direction.
        """
        valid_directions = ["UP", "DOWN"]
        if direction not in valid_directions:
            raise ValueError("Invalid direction. Use 'UP' or 'DOWN'.")
        key = Keys.ARROW_UP if direction == "UP" else Keys.ARROW_DOWN
        for _ in range(scroll_count):
            self.input.send_keys(key)
