# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

import time
from ..base_component import Selector
from .base_control import BaseControl
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class OAuthSelect(BaseControl):
    """
    Entity-Component: OAuthSelect

    OAuthSelect Javascript framework: OAuthSelect
    
    A dropdown which can select only one value
    """
    def __init__(self, browser, container, searchable=True):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """

        super(OAuthSelect, self).__init__(browser, container)
        self.elements.update({
            "values": Selector(select=container.select + ' [data-test="option"]'),
            "dropdown": Selector(select=container.select + ' .dropdownBox')
        })

    def select(self, value):
        """
        Selects the value within hte select dropdown
            :param value: the value to select
            :return: Bool if successful in selection, else raises an error
        """

        self.dropdown.click()
        popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
            "values":Selector(select=popoverid + ' [data-test="option"]:not([data-test-selected="true"]) [data-test="label"]')
        })
        for each in self.get_elements('values'):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def get_value(self):
        """
        Gets the selected value
            :return: Str The elected value within the dropdown, else returns blank
        """
        try:
            element = self.get_element("dropdown")
            return element.get_attribute("data-test-value")
        except:
            return ''

    def list_of_values(self):
        """
        Gets the list of value from the Single Select
            :returns: List of options from the single select
        """
        selected_val = self.get_value()
        self.container.click()
        first_element = None
        list_of_values = []
        popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
            "values":Selector(select=popoverid + ' [data-test="option"]')
        })
        for each in self.get_elements('values'):
            list_of_values.append(each.text.strip())
        return list_of_values    