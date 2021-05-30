# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

import time
from ..base_component import Selector
from .base_control import BaseControl
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class MultiSelect(BaseControl):
    """
    Entity-Component: Multiselect

    Select Javascript framework: select2
    
    A dropdown which can select more than one values
    """
    def __init__(self, browser, container):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in
        """
        super(MultiSelect, self).__init__(browser, container)

        self.elements.update({
            "internal_container": Selector(select=container.select + ' [role="listbox"]'),
            "dropdown": Selector(select=container.select + ' [role="listbox"]'),
            "selected": Selector(select=container.select + ' button[data-test="selected-option"][role="option"]'),
            "deselect": Selector(select=container.select + ' [data-test="crossmark"]'),
            "input": Selector(select=container.select +  ' [data-test="textbox"]'),
        })

    def search(self, value):
        """
        search with the multiselect input
            :param value: string value to search
        """
        self.input.send_keys(value)

    def search_get_list(self, value):
        """
        search with the multiselect input and return the list
            :param value: string value to search        
            :returns: list of values
        """
        self.search(value)
        self.wait_for_search_list()
        searched_values = list(self._list_visible_values())
        self.input.send_keys(Keys.ESCAPE)
        self.wait_for("container")
        return searched_values

    def select(self, value):
        """
        select a single value
            :param value: the value to select
            :return: Bool returns true if selection was successful, else raises an exception
        """
        try:
            self.input.click()
            popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")

        except:
            raise Exception("dropdown not found")

        self.elements.update({
            "values": Selector(select=popoverid + ' [data-test="option"]')
        })
        for each in self.get_elements('values'):
            if each.text.strip().lower() == value.lower():
                each.click()
                self.wait_for("input")
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def deselect(self, value):
        """
        Remove an item from selected list.
            :param value: the value to deselect
            :return: Bool returns true if deselect was successful, else raises an exception
        """
        for each in self.get_child_elements('selected'):
            if each.text.strip().lower() == value.lower():
                each.find_element(*list(self.elements["deselect"]._asdict().values())).click()
                self.wait_for("internal_container")
                return True
        else:
            raise ValueError("{} not found in select list".format(value))

    def deselect_all(self):
        """
        Remove all items from selected list.
        """
        for each in self.get_values():
            self.deselect(each)

    def get_values(self):
        """
        get list selected values
            :returns: List of values selected within the multi-select
        """
        return [each.text.strip() for each in self.get_child_elements("selected")]

    def list_of_values(self):
        """
        Get list of possible values to select from dropdown
            :returns: List of options within the multi-select dropdown
        """
        self.wait_for("internal_container")
        list_of_values = []

        self.input.click()
        popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
            "values": Selector(select=popoverid + ' [data-test="option"] [data-test="label"]')
        })
        for each in self.get_elements('values'):
            list_of_values.append(each.text.strip())
        return list_of_values
        
    def get_list_count(self):
        '''
            Gets the total count of the Multiselect list
        '''
        return len(list(self.list_of_values()))

    def _list_visible_values(self):
        """
        Get list of values which are visible. Used while filtering 
            :returns: List of visible options within the multi-select dropdown
        """
        self.input.click()
        popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
        "values": Selector(select=popoverid + ' [data-test="option"]:not([data-test-selected="true"]) [data-test="label"]')
        })
        for each in self.get_elements('values'):
            yield each.get_attribute('textContent')

    def wait_for_values(self):
        """
        Wait for dynamic values to load in Mulitple select
        """
        def _wait_for_values(driver):
            return self.get_list_count() > 0
        self.wait_for(_wait_for_values, msg="No values found in Multiselect")

    def wait_for_search_list(self):
        """
        Wait for Multiselect search to populate
        """
        def _wait_for_search_list(driver):
            return len(list(self._list_visible_values())) > 0
        self.wait_for(_wait_for_search_list, msg="No values found in Multiselect search")

    
