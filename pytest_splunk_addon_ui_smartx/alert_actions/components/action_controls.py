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

from lxml.cssselect import CSSSelector
from selenium.webdriver.common.by import By

from .alert_base_component import Selector
from .alert_base_control import AlertBaseControl


class ActionControls(AlertBaseControl):
    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
        :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        super().__init__(browser, container)
        select_xpath = CSSSelector(container.select).path
        self.elements.update(
            {
                "help_text": Selector(
                    by=By.XPATH,
                    select=select_xpath
                    + "//following::span[contains(@class, 'help-block')][1]",
                ),
                "label_text": Selector(
                    by=By.XPATH,
                    select=select_xpath
                    + "//preceding::label[contains(@class, 'control-label')][1]",
                ),
            }
        )
