# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ..base_component import Selector
from .base_control import BaseControl
from selenium.webdriver.common.by import By

class Toggle(BaseControl):
    """
    Entity_Component : Button
    """
    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The locator of the container where the control is located in. 
        """
        super(Toggle, self).__init__(browser, container)
        self.elements.update({
        "toggle_btn": Selector(select=container.select + " .btn"),
        "selected": Selector(select=container.select + " .active")
    })


    def select(self, value):
        for each in self.get_elements('toggle_btn'):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found".format(value))
    
    def get_value(self):
        return self.selected.text.strip()