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

import time

from selenium.common import exceptions
from selenium.webdriver.common.by import By

from .base_component import Selector
from .table import Table


class InputTable(Table):
    """
    Component: Input Table
    Input table has enable/disable, more-info views additionally to configuration table.
    """

    def __init__(self, browser, container, mapping={}):
        """
        :param browser: The selenium webdriver
        :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
        :param mapping: If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        super().__init__(browser, container, mapping)

        self.elements.update(
            {
                "switch_button_status": Selector(select='[data-disabled="true"]'),
                # It works as both selectors never exist simultaneously, if it does new_selector will get picked.
                "status_toggle": Selector(
                    select='button[data-test="toggle"][role="switch"], button[data-test="button"][role="switch"]'
                ),
                "switch_to_page": Selector(
                    select=container.select + " [data-test-page]"
                ),
                "input_status": Selector(
                    select=container.select
                    + ' [data-test="cell"][data-column="disabled"]'
                ),
            }
        )
        self.container = container

    def _get_status_button(self, name):
        """Find the status toggle button for the given input row."""
        _row = self._get_row(name)
        return _row.find_element(
            *list(self.elements["status_toggle"]._asdict().values())
        )

    def _is_input_enabled(self, name):
        """Return True if the input is currently enabled (data-selected == 'true')."""
        status_button = self._get_status_button(name)
        return (
            status_button.get_attribute("data-selected") or ""
        ).lower().strip() == "true"

    def input_status_toggle(self, name, enable):
        """
        This function sets the table row status as either enabled or disabled. If it is already enabled then it reuturns an exception
            :param name: Str The row that we want to enable st the status to as enabled or disabled
            :param enable: Bool Whether or not we want the table field to be set to enable or disable
            :return: Bool whether or not enabling or disabling the field was successful, If the field was already in the state we wanted it in, then it will return an exception
        """
        input_enabled = self._is_input_enabled(name)
        if enable:
            if input_enabled:
                raise Exception("The input is already enabled")
            else:
                self._get_status_button(name).click()
                # Wait for data-selected to reflect the new enabled state.
                # In UCC 6 (react-ui v5) the old [data-disabled="true"] spinner element
                # is not rendered; instead we poll data-selected directly.
                self.wait.until(lambda _: self._is_input_enabled(name))
                return True
        else:
            if not input_enabled:
                raise Exception("The input is already disabled")
            else:
                self._get_status_button(name).click()
                # Wait for data-selected to reflect the new disabled state.
                self.wait.until(lambda _: not self._is_input_enabled(name))
                return True
