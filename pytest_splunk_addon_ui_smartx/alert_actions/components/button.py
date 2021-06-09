# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ...components.controls.button import Button
from .alert_base_control import AlertBaseControl
from .action_controls import ActionControls

class Button(ActionControls):
    def __init__(self, browser, container):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """
        super(Button, self).__init__(browser, container)

    def click(self):
        """
        Click on the button
        """
        self.container.click()

    def wait_to_be_clickable(self):
        super(Button, self).wait_to_be_clickable("container")
