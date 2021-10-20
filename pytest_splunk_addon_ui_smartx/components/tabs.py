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

import time

from selenium.webdriver.common.by import By

from ..components.base_component import BaseComponent, Selector


class Tab(BaseComponent):
    """
    Component: Tab
    To change the tab in configuration page
    """

    def __init__(self, browser, container=Selector(select='[data-test="tab-bar"]')):
        """
        :param browser: The selenium webdriver
        :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
        """
        super().__init__(browser, container)
        self.elements.update(
            {
                "tab": Selector(select='[data-test="tab"][data-test-tab-id="{tab}"]'),
                "container": Selector(select='[data-test="tab-bar"]'),
            }
        )

    def open_tab(self, tab):
        """
        Open a specified tab
            :param tab: id of the tab
        """
        self.wait_for("container")
        tab_to_open = self._get_element(
            self.elements["tab"].by, self.elements["tab"].select.format(tab=tab).strip()
        )
        tab_to_open.click()
