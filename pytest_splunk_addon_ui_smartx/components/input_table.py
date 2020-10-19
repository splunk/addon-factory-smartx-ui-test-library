# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from .table import Table
from selenium.webdriver.common.by import By
from .base_component import Selector
import time
from selenium.common import exceptions


class InputTable(Table):
    """
    Component: Input Table
    Input table has enable/disable, more-info views additionally to configuration table.
    """
    def __init__(self, browser, container, mapping={}):
        super(InputTable, self).__init__(browser, container, mapping)

        self.elements.update({
            "switch_button_status":  Selector(select=" td.col-disabled .disabled"),
            "status_toggle":  Selector(select=" .switch-button .round"),
            "switch_to_page":  Selector(select=container.select + " .pull-right li a"),
            "input_status": Selector(select=container.select + " div.switch-label")
        })


    def input_status_toggle(self, name, enable):
        _row = self._get_row(name)
        input_status = _row.find_element(*list(self.elements["input_status"]._asdict().values()))
        status = input_status.text.strip().lower()
        if enable:
            if status == "enabled":
                raise Exception("The input is already {}".format(input_status.text.strip()))
            elif status == "disabled":
                status_button = _row.find_element(*list(self.elements["status_toggle"]._asdict().values()))
                status_button.click()
                self.wait_until("switch_button_status")
                return True
        else:
            if status == "disabled":
                raise Exception("The input is already {}".format(input_status.text.strip()))
            elif input_status.text.strip().lower() == "enabled":
                status_button = _row.find_element(*list(self.elements["status_toggle"]._asdict().values()))
                status_button.click()
                self.wait_until("switch_button_status")
                return True
            

