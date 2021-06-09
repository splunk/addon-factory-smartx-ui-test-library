# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.support.ui import Select
from .alert_base_component import AlertBaseComponent, Selector
from .alert_base_control import AlertBaseControl
from .action_controls import ActionControls

class AlertSingleSelect(ActionControls):
    def __init__(self, browser, container):
        super(AlertSingleSelect, self).__init__(browser, container)
        self.elements.update({
            "internal_container": Selector(select=container.select),
        })


    def select(self, value, open_dropdown=True):
        select_obj = Select(self.internal_container)
        select_obj.select_by_visible_text(value)
        return True

    def get_value(self):
        """
            Gets the selected value
        """
        select_obj = Select(self.internal_container)
        return self.get_clear_text(select_obj.first_selected_option)

    def list_of_values(self):
        """
            Gets the list of value from the Single Select
        """
        select_obj = Select(self.internal_container)
        value_list = []
        for each_obj in select_obj.options:
            value_list.append(self.get_clear_text(each_obj))

        return value_list
