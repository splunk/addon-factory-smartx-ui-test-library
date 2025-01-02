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

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ..base_component import Selector
from .base_control import BaseControl
from .button import Button

os_base = platform.system()


class Message(BaseControl):
    """
    Entity-Component: Message
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in.
        """
        super().__init__(browser, container)
        self.elements.update(
            {
                # changes w.r.t. splunk-ui 4.30.0
                "msg_text": Selector(
                    select=container.select
                    + '[data-test="message"] div[data-test="content"]'
                ),
            }
        )

    def get_msg(self):
        """
        Returns the error message
            :return: Str error message
        """
        return self.msg_text.text.strip()

    def wait_loading(self):
        """
        Wait till the message appears and then disappears
            :return: Str The text message after waiting
        """
        try:
            text = self.container.text
            self.wait_until("container")
            return text
        except:
            pass

    def wait_to_display(self):
        """
        Wait till the message appears
            :return: Str The text message after appearing
        """
        return self.container.text.strip()
