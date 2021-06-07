# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from .alert_base_component import AlertBaseComponent, Selector
from .action_controls import ActionControls

class ActionDropdown(ActionControls):

    def __init__(self, browser, container, mapping=dict()):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
            :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        super(ActionDropdown, self).__init__(browser, container)
        self.elements.update({
            "add_action": Selector(select=container.select + " .dropdown-toggle.btn"),
            "action_name": Selector(select=".unselected-action span:first-of-type"), 
        })

    def get_value_list(self):
        self.wait_to_be_clickable("add_action")
        self.add_action.click()
        value_list = []
        for each_action in self.get_elements("action_name"):
            if self.get_clear_text(each_action):
                value_list.append(self.get_clear_text(each_action))
        self.add_action.click()
        if not value_list:
            for each_action in self.get_elements("action_name"):
                if self.get_clear_text(each_action):
                    value_list.append(self.get_clear_text(each_action))
            self.add_action.click()
        return value_list

    def wait_for_values(self):
        """
        Wait for dynamic values to load in SingleSelect
        """
        def _wait_for_values(driver):
            return bool(self.get_value_list())
        self.wait_for(_wait_for_values, msg="No values found in the dropdown")

    def select_action(self, action_name):
        self.wait_to_be_clickable("add_action")
        self.add_action.click()
        value_list = []
        for each_action in self.get_elements("action_name"):
            if action_name == self.get_clear_text(each_action):
                each_action.click()
                break
            else:
                value_list.append(self.get_clear_text(each_action))
        else:
            self.add_action.click()
            raise ValueError("{} not found in Alert Action list. Founded list: {}".format(action_name, value_list))
