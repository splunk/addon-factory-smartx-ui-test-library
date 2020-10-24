# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ...components.controls.textbox import TextBox
from ...components.base_component import Selector

class AlertTextBox(TextBox):
    def __init__(self, browser, container):
        super(AlertTextBox, self).__init__(browser, container)
        self.elements.update({
            "input": Selector(select=container.select)
        })


