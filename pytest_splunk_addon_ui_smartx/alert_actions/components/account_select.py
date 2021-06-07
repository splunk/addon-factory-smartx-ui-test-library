# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from selenium.common.exceptions import TimeoutException
from .action_controls import ActionControls
from .alert_base_component import AlertBaseComponent, Selector
from .alert_base_control import AlertBaseControl
from selenium.webdriver.common.keys import Keys

class AlertAccountSelect(ActionControls):
    def __init__(self, browser, container):
        super(AlertAccountSelect, self).__init__(browser, container)
        self.elements.update({
            "internal_container": Selector(select=container.select + " .splunk-dropdown"),
            "dropdown": Selector(select=container.select + ' button[data-is-menu="true"]'),
            "selected": Selector(select=container.select + ' button[data-is-menu="true"] span[data-test="label"]'),
            "values": Selector(select='div[data-test="popover"] button[data-test="option"]'),
            "cancel_selected": Selector(select=container.select + ' button[data-icon-only="true"]')
        })

    def wait_for_values(self):
        """
        Wait for dynamic values to load in SingleSelect
        """
        def _wait_for_values(driver):
            try:
                return self.get_single_value()
            except Exception as e:
                print("Wait_for_values failed with ::{}".format(str(e)))
        try:
            self.wait_for(_wait_for_values, msg="No values found in SingleSelect")
        except TimeoutException:
            return True

    def list_of_values(self):
        """
            Gets the list of value from the Single Select
        """
        self.wait_to_be_clickable("dropdown")
        self.dropdown.click()
        list_of_values = []
        for each in self.get_elements('values'):
            list_of_values.append(each.text.strip())
        self.wait_to_be_clickable("dropdown")
        self.dropdown.click()
        self.wait_for("internal_container")
        return list_of_values

    def get_single_value(self):
        """
        Return one value from Single Select 
        """
        self.wait_to_be_clickable("dropdown")
        self.dropdown.click()
        single_element = self.get_element('values')

        self.wait_to_be_clickable("dropdown")
        self.dropdown.click()
        self.wait_for("internal_container")
        return single_element

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

        # assert self.searchable, "Can not search, as the Singleselect is not searchable"
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

    def get_list_count(self):
        '''
        Gets the total count of the SingleSelect list
            :return: Int the count of the options within the Single Select
        '''
        return len(list(self.list_of_values()))

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
