# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

import time
from ..base_component import Selector
from .base_control import BaseControl
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SingleSelect(BaseControl):
    """
    Entity-Component: SingleSelect
    Select Javascript framework: select2
    A dropdown which can select only one value
    """
    def __init__(self, browser, container, searchable=True):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """

        super(SingleSelect, self).__init__(browser, container)
        self.searchable = searchable
        self.elements.update({
            "internal_container": Selector(select=container.select + " div.select2-container"),
            "dropdown": Selector(select=container.select + " .select2-choice"),
            "selected": Selector(select=container.select + " .select2-choice:not(.select2-default)"),
            "values": Selector(select='.select2-drop-active[style*="display: block;"] .select2-result-selectable'),
            "cancel_selected":Selector(select=container.select + ' .select2-search-choice-close')
            # To update
        })

        if searchable:
            self.elements.update({
                "input": Selector(select='.select2-with-searchbox.select2-drop-active[style*="display: block;"] .select2-input')
            })

    def select(self, value, open_dropdown=True):
        """
        Selects the value within the select dropdown
            :param value: the value to select
            :param open_dropdown: Bool Whether to open the the dropwdown or not 
            :return: Bool if successful in selection, else raises an error
        """
        if open_dropdown:
            self.wait_to_be_clickable("dropdown")
            self.dropdown.click()
        
        for each in self.get_elements('values'):
            if each.text.strip().lower() == value.lower():
                each.click()
                self.wait_for('internal_container')
                return True
        else:
            raise ValueError("{} not found in select list".format(value))


    def search(self, value):
        """
        search with the singleselect input
            :param value: string value to search
            :assert: Asserts whether or not the single select is seachable
        """

        assert self.searchable, "Can not search, as the Singleselect is not searchable"
        self.dropdown.click()

        #DEBUG: maybe we have to click the select button
        self.input.send_keys(value)

    def search_get_list(self, value):
        """
        search with the singleselect input and return the list
            :param value: string value to search        
            :returns: list of values
        """

        self.search(value)
        self.wait_for_search_list()
        searched_values = list(self._list_visible_values())
        self.input.send_keys(Keys.ESCAPE)
        self.wait_for("container")
        return searched_values

    def _list_visible_values(self):
        """
        Gets list of values which are visible. Used while filtering
            :returns: List of the values that are visible
        """
        for each in self.get_elements('values'):
            yield each.get_attribute('textContent')


    def get_value(self):
        """
        Gets the selected value
            :return: The selected value's text, or returns false if unsuccessful
        """
        try:
            self.wait_for_text("selected")
            return self.selected.text.strip()
        except:
            return False
      
    def get_placeholder_value(self):
        """
        get placeholder value from the single select
        """
        return self.input.get_attribute('placeholder').strip()

    def cancel_selected_value(self):
        '''
        Cancels the currently selected value in the SingleSelect
            :return: Bool whether or not canceling the selected item was successful, else raises a error
        '''
        try:
            self.wait_to_be_clickable("cancel_selected")
            self.cancel_selected.click()
            return True
        except:
            raise ValueError("No selected value")

    def list_of_values(self):
        """
        Gets the list of value from the Single Select
            :returns: list of options avaialble within the single select
        """
        selected_val = self.get_value()
        self.dropdown.click()
        first_element = None
        list_of_values = []
        for each in self.get_elements('values'):
            if not first_element:
                first_element = each
            list_of_values.append(each.text.strip())
        if selected_val:
            self.select(selected_val, open_dropdown=False)
        elif self.searchable:
            self.input.send_keys(Keys.ESCAPE)
        elif first_element:
            self.select(first_element.text.strip(), open_dropdown=False)
        self.wait_for("internal_container")
        return list_of_values

    def get_single_value(self):
        """
        Return one value from Single Select 
        """
        selected_val = self.get_value()
        self.dropdown.click()
        first_element = None
        single_element = self.get_element('values')
        if selected_val:
            self.select(selected_val, open_dropdown=False)
        elif self.searchable:
            self.input.send_keys(Keys.ESCAPE)
        elif first_element:
            self.select(first_element.text.strip(), open_dropdown=False)
        self.wait_for("internal_container")
        return single_element

    def get_list_count(self):
        '''
        Gets the total count of the SingleSelect list
            :return: Int the count of the options within the Single Select
        '''
        return len(list(self.list_of_values()))

    def wait_for_values(self):
        """
        Wait for dynamic values to load in SingleSelect
        """
        def _wait_for_values(driver):
            return self.get_single_value()
        self.wait_for(_wait_for_values, msg="No values found in SingleSelect")

    def wait_for_search_list(self):
        """
        Wait for SingleSelect search to populate
        """
        def _wait_for_search_list(driver):
            return len(list(self._list_visible_values())) > 0
        self.wait_for(_wait_for_search_list, msg="No values found in SingleSelect search")

    def is_editable(self):
        '''
        Returns True if the Textbox is editable, False otherwise
        '''
        return not bool(self.input.get_attribute("readonly") or self.input.get_attribute("readOnly") or self.input.get_attribute("disabled"))
