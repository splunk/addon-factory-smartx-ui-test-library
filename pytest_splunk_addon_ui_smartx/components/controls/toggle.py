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
        self.elements.update(
            {
                "toggle_btn": Selector(
                    select=container.select + ' [data-test="option"] [data-test="label"]'
                ),
                "selected": Selector(
                    select=container.select + ' [data-test="option"][aria-checked="true"] [data-test="label"]'
                )
            }
        )
        self.browser = browser
        self.container = container

    def select(self, value):
        """
        Selects the toggle specified
            :param value: the value to select
            :return: Bool if successful in selection, else raises an error
        """
        for each in self.get_elements('toggle_btn'):
            if each.text.lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found".format(value))
    
    def get_value(self):
        """
        Returns the value of the toggle element
            :return: Str the text for the toggle element
        """
        return self.selected.text.strip()