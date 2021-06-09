# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from .base_component import BaseComponent, Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
from selenium.common import exceptions

class Dropdown(BaseComponent):
    """
    Component: Dropdown
    Base class of Input & Configuration table
    """
    def __init__(self, browser, container, mapping=dict()):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
            :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        super(Dropdown, self).__init__(browser, container)
        self.elements.update({
            "currunt_value": Selector(select=container.select + ' [data-test="select"] [data-test="label"]'),
            "pagination_dropdown": Selector(select='button[data-test="select"]'),
            "type_dropdown": Selector(select=container.select),
            "add_input": Selector(by=By.ID, select='addInputBtn'),
            "type_filter_list":Selector(select='button[data-test="option"]')
        })

    def select_page_option(self, value):
        """
        Selects the page option that the user specifies in value
            :param value: The value in which we want to select
            :return: Returns True if successful, otherwise raises an error
        """
        self.pagination_dropdown.click()
        popoverid = '#' + self.pagination_dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
            "page_list": Selector(select=popoverid + ' [data-test="label"]'),
        })
        for each in self.get_elements('page_list'):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def get_value(self):
        """
        Returns the current value for the dropdown
            :return: Str The current value for the dropdown
        """
        return self.currunt_value.text.strip()

    def select(self, value):
        """
        Selects the value we want from the type list
            :param value: The value in which we want to select
            :return: Returns True if successful, otherwise raises an error
        """

        self.add_input.click()
        popoverid = '#'+ self.add_input.get_attribute("data-test-popover-id")
        self.elements.update({
            "values": Selector(select=popoverid + ' [data-test="item"]:not([data-test-selected="true"]) [data-test="label"]')
        })
        for each in self.get_elements('values'):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def select_input_type(self, value, open_dropdown=True):
        """
        Selects the input type option that the user specifies in value
            :param value: The value in which we want to select
            :param open_dropdown: Whether or not the dropdown should be opened
            :return: Returns True if successful, otherwise raises an error
        """
        if open_dropdown:
            self.type_dropdown.click()
        popoverid = '#' + self.type_dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
            "type_filter_list": Selector(select=popoverid + ' [data-test="label"]'),
        })
        for each in self.get_elements('type_filter_list'):
            if each.text.strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def get_inputs_list(self):
        """
        Returns a generator list for the options available in the add input dropdown
            :return: Returns Generator list of values 
        """
        self.add_input.click()
        popoverid = '#' + self.add_input.get_attribute("data-test-popover-id")
        self.elements.update({
            "type_list": Selector(select=popoverid + ' [data-test="item"]'),
        })
        return [each.text.strip() for each in self.get_elements("type_list")]

    def get_pagination_list(self):
        """
        Returns a generator list for the pagination text available in the add input dropdown
            :return: Returns Generator list of values 
        """
        self.pagination_dropdown.click()
        popoverid = '#' + self.pagination_dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
            "page_list": Selector(select=popoverid + ' [data-test="label"]'),
        })
        return [each.text.strip() for each in self.get_elements("page_list")]

    def get_input_type_list(self):
        """
        Returns a generator list for the input types available in the add input dropdown
            :return: Returns Generator list of values 
        """
        self.type_dropdown.click()
        popoverid = '#' + self.type_dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
            "type_filter_list": Selector(select=popoverid + ' [data-test="label"]'),
        })
        return [each.text.strip() for each in self.get_elements("type_filter_list")]

        
        