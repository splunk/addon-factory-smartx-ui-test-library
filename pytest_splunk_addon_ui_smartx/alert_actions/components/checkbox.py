# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ...components.controls.checkbox import Checkbox
from ...components.base_component import Selector
class AlertCheckbox(Checkbox):
    def __init__(self, browser, container):
        super(AlertCheckbox, self).__init__(browser, container, searchable=False)
        self.elements.update({
            "checkbox": Selector(select=container.select)
        })


    def is_checked(self):
        '''
        Returns True if the checkbox is already checked, otherwise False
        '''
        return self.checkbox.is_selected()
       