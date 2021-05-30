# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from ..base_component import Selector
from .base_control import BaseControl
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .button import Button
import platform

os_base = platform.system()

class Message(BaseControl):
    """
    Entity-Component: Message
    """
    def __init__(self, browser, container):
        """
            :param browser: The selenium webdriver
            :param container: The locator of the container where the control is located in. 
        """
        super(Message, self).__init__(browser, container)  
        self.elements.update({
            "msg_text": Selector(select=container.select + '[data-test="message"]'),
            "input": Selector(select='[data-test="control-group"] [data-test="textbox"]')
        })



    def get_msg(self):
        '''
        Returns the error message
            :return: Str error message
        '''
        return self.msg_text.text.strip()

    def close_msg(self):
        """
        Cancel the error message 
            :return: Bool if successful
        """
        text_value = self.get_value()
        self.input.send_keys("a")
        if os_base == 'Darwin':
            self.input.send_keys(Keys.COMMAND, 'a')
        else:
            self.input.send_keys(Keys.CONTROL, 'a')
        self.input.send_keys(Keys.DELETE)
        self.input.send_keys(text_value)
        return True

    def wait_loading(self):
        """
        Wait till the message appears and then dissapears
            :return: Str The text message after waiting
        """
        try:
            text = self.container.text
            self.wait_until("container")
            return text
        except:
            pass

    def wait_to_display(self):
        """
        Wait till the message appears
            :return: Str The text message after appearing
        """
        return self.container.text.strip()

    def get_value(self):
        """
        get value from the textbox
            :return: Str The current value of the textbox
        """
        return self.input.get_attribute('value').strip()
        
