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
                "status_toggle": Selector(
                    select='button[data-test="button"][role="switch"]'
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

    def input_status_toggle(self, name, enable):
        """
        This function sets the table row status as either enabled or disabled. If it is already enabled then it reuturns an exception
            :param name: Str The row that we want to enable st the status to as enabled or disabled
            :param enable: Bool Whether or not we want the table field to be set to enable or disable
            :return: Bool whether or not enabling or disabling the field was successful, If the field was already in the state we wanted it in, then it will return an exception
        """
        _row = self._get_row(name)
        input_status = _row.find_element(
            *list(self.elements["input_status"]._asdict().values())
        )
        status = (
            input_status.find_element_by_css_selector('[data-test="status"]')
            .text.strip()
            .lower()
        )
        status_button = _row.find_element(
            *list(self.elements["status_toggle"]._asdict().values())
        )
        if enable:
            if status == "enabled":
                raise Exception(
                    "The input is already {}".format(self.input_status.text.strip())
                )
            elif status == "disabled":
                status_button.click()
                self.wait_until("switch_button_status")
                return True
        else:
            if status == "disabled":
                raise Exception(
                    "The input is already {}".format(self.input_status.text.strip())
                )
            elif status == "enabled":
                status_button.click()
                self.wait_until("switch_button_status")
                return True
