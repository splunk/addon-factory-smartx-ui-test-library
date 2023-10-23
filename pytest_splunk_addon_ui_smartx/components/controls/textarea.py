#
# Copyright 2021 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
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

    def get_placeholder_value(self):
        """
        get placeholder value from the textbox
            :return: Str Value of the placeholder
        """
        return self.input.get_attribute("placeholder")

    def get_textarea_height(self) -> int:
        """
        Get the height of the displayed textarea.
            :return: Int Height of the textarea in pixels.
        """
        style = self.input.get_attribute("style")
        if "height" in style:
            styles = style.split(";")
            for s in styles:
                if "height" in s:
                    height = int(s.split(":")[-1].strip().replace("px", ""))
                    return height
        return 0

    def append_value(self, value):
        """
        Appends the specified 'value' to an textarea element
        """
        self.input.send_keys(value)
