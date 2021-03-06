# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from ..pages.page import Page
from selenium.webdriver.common.by import By
from abc import abstractmethod
from .controls.button import Button
from .controls.message import Message
from .base_component import BaseComponent, Selector
from .dropdown import Dropdown
import time

class Entity(BaseComponent):
    """
    Entity form to add/edit the configuration.
    The instance of the class expects that the entity is already open.
    The instance of the class holds all the controls in the entity and provides the generic interaction that can be done with the entity
    """
    
    def __init__(self, browser, container, add_btn=None):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the Entity is located. Of type dictionary: {"by":..., "select":...}
            :param add_btn: The locator of add_button with which the entity will be opened
        """
        self.browser = browser
        super(Entity, self).__init__(browser, container)
        
        # Controls
        self.save_btn = Button(browser, Selector(select=container.select + " input.submit-btn"))
        self.loading = Message(browser,  Selector(select=container.select + " .msg-loading"))
        self.add_btn = add_btn
        self.msg_error = Message(browser,  Selector(select=" .msg-error"))
        self.msg_warning = Message(browser,  Selector(select=" .msg-warning"))
        self.cancel_btn = Button(browser,  Selector(select=container.select + " button.cancel-btn" ))
        self.close_btn = Button(browser,  Selector(select=container.select + " button.close" ))
        self.create_new_input = Dropdown(browser,  Selector(select=" .add-button"))
        
    def get_warning(self):
        """
        Get the error message displayed while saving the configuration
        """
        return self.msg_warning.get_msg()

    def get_error(self):
        """
        Get the error message displayed while saving the configuration
        """
        return self.msg_error.get_msg()

    def close_error(self):
        return self.msg_error.close_msg()

    def save(self, expect_error=False, expect_warning=False):
        """
        Save the configuration
            :param expect_error: if True, the error message will be fetched.
            :param expoect_warning: If True, the warning message will be fetched.
            :returns: If expect_error or expect_warning is True, then it will return the message appearing on page. 
                       Otherwise, the function will return True if the configuration was saved properly
        """
        self.save_btn.wait_to_be_clickable()
        self.save_btn.click()
        if expect_error:
            return self.get_error()
        elif expect_warning:
            return self.get_warning()
        else:
            self.loading.wait_loading()
            return True

    def cancel(self):
        """
        Cancel the entity
            :return: True if done properly
        """
        self.cancel_btn.click()
        self.save_btn.wait_until("container")
        return True

    def close(self):
        """
        Close the entity 
            :return: True if done properly
        """
        self.close_btn.click()
        self.save_btn.wait_until("container")
        return True

    def open(self):
        """
        Open the entity by click on "New" button. 
            :return: True if done properly
        """
        self.add_btn.click()
        self.save_btn.wait_to_display()
        return True


