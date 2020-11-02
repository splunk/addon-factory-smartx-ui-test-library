# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from selenium.common.exceptions import TimeoutException
from ...components.controls.single_select import SingleSelect
from ...components.base_component import Selector, BaseComponent

class AlertAccountSelect(SingleSelect):
    def __init__(self, browser, container):
        super(AlertAccountSelect, self).__init__(browser, container, searchable=False)
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