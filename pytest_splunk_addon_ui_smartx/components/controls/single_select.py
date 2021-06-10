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

    A dropdown which can select only one value
    """
    def __init__(self, browser, container, searchable=True, allow_new_values=False):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
            :param searchable: Boolean indicating if the dropdown provides filter or not.
            :param allow_new_values: Boolean indicating if the dropdown allows for user entered custom values excluding predefined list.
        """
        super(SingleSelect, self).__init__(browser, container)
        self.searchable = searchable
        # Component is ComboBox in case of True
        self.allow_new_values = allow_new_values
        self.container = container
        self.elements.update({
            "internal_container": Selector(select=container.select + ' .dropdownBox'),
            "dropdown": Selector(select=container.select + ' .dropdownBox'),
            "combobox":Selector(select=container.select + ' [data-test="combo-box"]'),
            "selected":Selector(select=container.select + ' [data-test="textbox"]'),
            "cancel_selected":Selector(select=container.select + ' [data-test="clear"]'),
            })
        if not self.searchable and self.allow_new_values:
            raise ValueError("Invalid combination of values for searchable and allow_new_values flags")

    def select(self, value, open_dropdown=True):
        """
        Selects the value within the select dropdown
            :param value: the value to select
            :param open_dropdown: Whether or not the dropdown should be opened
            :return: Bool if successful in selection, else raises an error
        """
        if open_dropdown: 
            self.wait_to_be_clickable("dropdown")
            self.dropdown.click()

        if self.allow_new_values:
            if self.get_value():
                self.cancel_selected.click()
            popoverid = '#' + self.combobox.get_attribute("data-test-popover-id")
        else:
            popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
        self.elements.update({
            "values": Selector(select=popoverid + ' [data-test="option"]')
        })

        for each in self.get_elements('values'):
            if each.text.strip().lower() == value.lower():
                each.click()
                self.wait_for('internal_container')
                return True
        else:
            raise ValueError("{} not found in select list".format(value))


    def search(self, value, open_dropdown=True):
        """
        search with the singleselect input
            :param value: string value to search
            :assert: Asserts whether or not the single select is seachable
        """
        assert self.searchable, "Can not search, as the Singleselect is not searchable"
        if open_dropdown:
            self.wait_to_be_clickable("dropdown")
            self.dropdown.click()
        if self.searchable:
            if self.allow_new_values:
                self.elements.update({
                    "input": Selector(select=self.container.select + ' [data-test="textbox"]')
                })
            else:
                popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
                self.elements.update({
                    "input": Selector(select= popoverid + ' [data-test="textbox"]')
                })

        #DEBUG: maybe we have to click the select button
        self.input.send_keys(value)

    def search_get_list(self, value):
        """
        search with the singleselect input and return the list
            :param value: string value to search        
            :returns: list of values
        """

        if self.searchable:
            if self.allow_new_values:
                self.elements.update({
                    "input": Selector(select=self.container.select + ' [data-test="textbox"]')
                })
            else:
                self.dropdown.click()
                popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
                self.elements.update({
                    "input": Selector(select= popoverid + ' [data-test="textbox"]')
                })
        # as the dropdown is already open we dont try to open it
        self.search(value, open_dropdown=False)
        if self.allow_new_values:
            searched_values = list(self._list_visible_values())
        else:
            self.wait_for_search_list()
            searched_values = list(self._list_visible_values(open_dropdown=False))
            self.input.send_keys(Keys.ESCAPE)
            self.wait_for("container")
        return searched_values

    def _list_visible_values(self, open_dropdown=True):
        """
        Gets list of values which are visible. Used while filtering
            :param open_dropdown: Whether or not the dropdown should be opened
            :returns: List of the values that are visible
        """
        if open_dropdown:
            self.dropdown.click()
        if self.allow_new_values:
            popoverid = '#' + self.combobox.get_attribute("data-test-popover-id")
            self.elements.update({
                "values":Selector(select=popoverid + ' [data-test="option"]')
            })
        else:
            popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
            self.elements.update({
                "values":Selector(select=popoverid + ' [data-test="option"]:not([data-test-selected="true"]) [data-test="label"]')
            })
        for each in self.get_elements('values'):
            yield each.get_attribute('textContent')


    def get_value(self):
        """
        Gets the selected value
            :return: The selected value's text, or returns false if unsuccessful
        """
        if self.allow_new_values:
            # ComboBox do not support label
            return self.selected.get_attribute("value")
        else:
            if (self.dropdown.get_attribute("data-test-loading") == "false"
                    and self.dropdown.get_attribute("data-test-value")):
                return self.dropdown.get_attribute("label")
            else:
                return False

    def get_placeholder_value(self):
        """
        get placeholder value from the single select
        """
        if self.searchable:
            if self.allow_new_values:
                self.elements.update({
                    "input": Selector(select=self.container.select + ' [data-test="textbox"]')
                })
            else:
                self.dropdown.click()
                popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
                self.elements.update({
                    "input": Selector(select= popoverid + ' [data-test="textbox"]')
                })

        return self.input.get_attribute('placeholder').strip()

    def cancel_selected_value(self):
        '''
        Cancels the currently selected value in the SingleSelect
            :return: Bool whether or not canceling the selected item was successful, else raises a error
        '''
        try:
            self.dropdown.click()
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

        if self.allow_new_values:
            if self.searchable:
                self.elements.update({
                    "input": Selector(select=self.container.select + ' [data-test="textbox"]')
                })
            popoverid = '#' + self.combobox.get_attribute("data-test-popover-id")
        else:
            popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
            if self.searchable:
                self.elements.update({
                        "input": Selector(select=popoverid + ' [data-test="textbox"]')
                    })
        self.elements.update({
            "values":Selector(select=popoverid + ' [data-test="option"]')
        })
        
        for each in self.get_elements('values'):
            if not first_element:
                first_element = each
            list_of_values.append(each.text.strip())
        if selected_val and not self.allow_new_values:
            # as the dropdown is already open we dont try to open it
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
        first_element = None

        self.wait_to_be_clickable("dropdown")
        self.dropdown.click()
        if self.allow_new_values:
            if self.searchable:
                self.elements.update({
                    "input": Selector(select=self.container.select + ' [data-test="textbox"]')
                })
            popoverid = '#' + self.combobox.get_attribute("data-test-popover-id")
            self.elements.update({
                "values":Selector(select=popoverid + ' [data-test="option"]:not([data-test-selected="true"]) [data-test="label"]')
            })
        else:
            if self.searchable:
                popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
                self.elements.update({
                    "input": Selector(select=popoverid + ' [data-test="textbox"]')
                })
            popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
            self.elements.update({
                "values":Selector(select= popoverid + ' [data-test="option"]')
            })

        single_element = self.get_element("values")

        if selected_val and not self.allow_new_values:
            # as the dropdown is already open we dont try to open it
            self.select(selected_val, open_dropdown=False)
        elif self.searchable:
            self.input.send_keys(Keys.ESCAPE)
        else:
            self.select(single_element.text.strip(), open_dropdown=False)
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
            return len(list(self._list_visible_values(open_dropdown=False))) > 0
        self.wait_for(_wait_for_search_list, msg="No values found in SingleSelect search")

    def is_editable(self):
        '''
        Returns True if the Textbox is editable, False otherwise
        '''
        if self.searchable:
            if self.allow_new_values:
                self.elements.update({
                    "input": Selector(select=self.container.select + ' [data-test="textbox"]')
                })
            else:
                self.dropdown.click()
                popoverid = '#' + self.dropdown.get_attribute("data-test-popover-id")
                self.elements.update({
                    "input": Selector(select= popoverid + ' [data-test="textbox"]')
                })
        return not bool(self.input.get_attribute("readonly") or self.input.get_attribute("readOnly") or self.input.get_attribute("disabled"))
