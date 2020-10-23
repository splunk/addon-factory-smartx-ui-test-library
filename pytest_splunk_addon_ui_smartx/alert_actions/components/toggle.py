# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ...components.controls.toggle import Toggle
from ...components.base_component import Selector

class AlertToggle(Toggle):
    def __init__(self, browser, container):
        super(AlertToggle, self).__init__(browser, container)
        self.elements.update({
            "toggle_btn": Selector(select=container.select),
        })


    def select(self, value):
        for each in self.get_elements('toggle_btn'):
            if each.get_attribute("value").strip().lower() == value.lower():
                each.click()
                return True
        else:
            raise ValueError("{} not found".format(value))

    def get_value(self):
        for each in self.get_elements('toggle_btn'):
            if each.is_selected():
                return each.get_attribute("value")
