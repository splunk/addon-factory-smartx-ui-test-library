# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from .alert_base_component import Selector
from .alert_base_control import AlertBaseControl
from .action_controls import ActionControls

class AlertToggle(ActionControls):
    def __init__(self, browser, container):
        super(AlertToggle, self).__init__(browser, container)
        self.elements.update({
            "toggle_btn": Selector(select=container.select),
            "selected": Selector(select=container.select + " .active")
        })

    def select(self, value):
        """
        Selects the toggle specified
            :param value: the value to select
            :return: Bool if successful in selection, else raises an error
        """
        for each in self.get_elements('toggle_btn'):
            if each.get_attribute("value").strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found".format(value))
    
    def get_value(self):
        for each in self.get_elements('toggle_btn'):
            if each.is_selected():
                return each.get_attribute("value")
