# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from .alert_base_component import Selector
from .alert_base_control import AlertBaseControl
from .action_controls import ActionControls

class AlertCheckbox(ActionControls):
    def __init__(self, browser, container):
        super(AlertCheckbox, self).__init__(browser, container)
        self.elements.update({
            "internal_container": Selector(select=container.select + " div.select2-container"),
            "checkbox": Selector(select=container.select),
            "checkbox_btn": Selector(select=container.select + " .checkbox a.btn"),
            "checkbox_enabled": Selector(select=container.select + ' .checkbox a.btn .icon-check')
        })

    
    def toggle(self):
        '''
        Toggles the checkbox value
        '''
        self.wait_to_be_clickable("checkbox")
        self.checkbox.click()

    def check(self):
        '''
        Checks the checkbox if unchecked
            :return: Bool true if successful, else it will return a statement that it was already checked
        '''
        try:
            if self.is_checked() == False:
                self.toggle()
            return True
        except:
            return "Checkbox is already checked"

    def uncheck(self):
        '''
        Unchecks the checkbox if checked
            :return: Bool true if successful, else it will return a statement that it was already unchecked
        '''
        try:
            if self.is_checked() == True:
                self.toggle()
            return True
        except:
            return "Checkbox is already unchecked"

    def is_checked(self):
        '''
        Returns True if the checkbox is already checked, otherwise False
            :return: Bool True if checked, False if unchecked
        '''
        return self.checkbox.is_selected()
       