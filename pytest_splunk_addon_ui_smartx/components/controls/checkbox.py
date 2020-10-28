# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

import time
from ..base_component import Selector
from .base_control import BaseControl
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Checkbox(BaseControl):
    """
    Entity_Component : Checkbox
    """

    def __init__(self, browser, container, searchable=True):
        super(Checkbox, self).__init__(browser, container)
        self.elements.update({
            "internal_container": Selector(select=container.select + " div.select2-container"),
            "checkbox": Selector(select=container.select + ' .checkbox'),
            "checkbox_btn": Selector(select=container.select + " .checkbox a.btn"),
            "checkbox_enabled": Selector(select=container.select + ' .checkbox a.btn .icon-check')
        })

    
    def toggle(self):
        '''
        Toggles the checkbox value
        '''
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
        element = self.get_element("checkbox_enabled")
        a = element.value_of_css_property("display")
        if a =="inline-block":
            return True
        else:
            return False
    
