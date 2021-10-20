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

from selenium.webdriver.common.action_chains import ActionChains

from .action_controls import ActionControls
from .alert_base_component import Selector
from .textbox import AlertTextBox


class SearchBox(ActionControls):
    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        """
        super().__init__(browser, container)
        self.elements.update(
            {
                "text_container": Selector(select=container.select + " .ace_editor"),
                "text_content": Selector(select=container.select + " .ace_content"),
            }
        )
        self.action_chain = ActionChains(self.browser)

    def set_value(self, value):
        self.text_container.click()
        self.action_chain.send_keys(value)
        self.action_chain.perform()

    def get_value(self):
        return self.get_clear_text(self.text_content)
