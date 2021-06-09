# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from selenium.webdriver.common.action_chains import ActionChains
from .textbox import AlertTextBox
from .alert_base_component import Selector
from .action_controls import ActionControls

class SearchBox(ActionControls):
    def __init__(self, browser, container):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """
        super(SearchBox, self).__init__(browser, container)
        self.elements.update({
            "text_container": Selector(select=container.select + " .ace_editor"),
            "text_content": Selector(select=container.select + " .ace_content")
        })
        self.action_chain = ActionChains(self.browser)

    def set_value(self, value):
        self.text_container.click()
        self.action_chain.send_keys(value)
        self.action_chain.perform()

    def get_value(self):
        return self.get_clear_text(self.text_content)
