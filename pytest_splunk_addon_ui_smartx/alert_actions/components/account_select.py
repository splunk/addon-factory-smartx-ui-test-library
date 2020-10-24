# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

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


    def list_of_values(self):
        """
            Gets the list of value from the Single Select
        """
        self.wait_to_be_clickable("dropdown")
        self.dropdown.click()
        list_of_values = []
        for each in self.get_elements('values'):
            list_of_values.append(each.text.strip())
        self.dropdown.click()
        self.wait_for("internal_container")
        self.wait_to_be_clickable("dropdown")
        return list_of_values
