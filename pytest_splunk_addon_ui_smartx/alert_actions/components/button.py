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

from ...components.controls.button import Button
from .action_controls import ActionControls
from .alert_base_control import AlertBaseControl


class Button(ActionControls):
    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        """
        super().__init__(browser, container)

    def click(self):
        """
        Click on the button
        """
        self.container.click()

    def wait_to_be_clickable(self):
        super().wait_to_be_clickable("container")
