# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0
from .base_control import BaseControl
from ..base_component import Selector
from selenium.webdriver.common.keys import Keys
import platform

os_base = platform.system()

class TextBox(BaseControl):
    """
    Entity-Component: TextBox
    """

    def __init__(self, browser, container, encrypted=False):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """
        super(TextBox, self).__init__(browser, container)
        self.encrypted = encrypted
        self.container = container
        self.browser = browser
        self.elements.update(
            {"input": Selector(select=container.select + ' input')}
        )

    def set_value(self, value):
        """
        set value of the textbox
        """
        # first condition added for safari browser
        if self.browser.capabilities["browserName"] == "Safari":
            self.input.send_keys(Keys.COMMAND)
            self.input.send_keys('a')
        elif os_base == 'Darwin':
            self.input.send_keys(Keys.COMMAND, 'a')
        else:
            self.input.send_keys(Keys.CONTROL, 'a')
        self.input.send_keys(Keys.DELETE)
        self.input.send_keys(value)

    def get_value(self):
        """
        get value from the textbox
            :return: Str The current value of the textbox
        """
        return self.input.get_attribute('value').strip()

    def get_placeholder_value(self):
        """
        get placeholder value from the textbox
        """
        return self.input.get_attribute('placeholder').strip()

    def is_editable(self):
        '''
        Returns True if the Textbox is editable, False otherwise
            :return: Bool whether or not the textbox is editable
        '''
        return not bool(self.input.get_attribute("readonly") or self.input.get_attribute("disabled"))


    def clear_text(self):
        '''
        Clears the textbox value
        '''
        self.input.clear()

    def get_type(self):
        '''
        Get type of value entered in textbox
            :return: Type of input within the textbox
        '''
        return self.input.get_attribute('type').strip()

    def wait_to_be_editable(self):
        """
        Wait for the textbox field to be editable
        """
        def _wait_for_field_to_be_editable(driver):
            return self.is_editable == True
        self.wait_for(_wait_for_field_to_be_editable, msg="Field is uneditable")
