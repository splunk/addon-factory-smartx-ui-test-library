#
# Copyright 2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Union

import selenium.common
from selenium.webdriver.common.by import By

from .base_component import BaseComponent, Selector
from .controls.button import Button
from .controls.message import Message
from .dropdown import Dropdown

import warnings


class Entity(BaseComponent):
    """
    Entity form to add/edit the configuration.
    The instance of the class expects that the entity is already open.
    The instance of the class holds all the controls in the entity and provides the generic interaction that can be done with the entity
    """

    def __init__(self, browser, container, add_btn=None, is_single_page=False):
        """
        :param browser: The selenium webdriver
        :param container: Container in which the Entity is located. Of type dictionary: {"by":..., "select":...}
        :param add_btn: The locator of add_button with which the entity will be opened
        :param is_single_page: Boolean indicating whether the selected tab is single entity form or not like proxy and logging.
        """
        self.browser = browser
        super().__init__(browser, container)

        # Controls
        self.save_btn = Button(browser, Selector(select=container.select + " .saveBtn"))
        self.loading = Message(
            browser,
            Selector(select=container.select + ' button[data-test="wait-spinner"]'),
        )
        if not is_single_page:
            self.add_btn = add_btn
        self.msg_error = Message(
            browser, Selector(select='div[data-test-type="error"]')
        )
        self.msg_warning = Message(
            browser, Selector(select='div[data-test-type="warning"]')
        )
        self.msg_markdown = Message(
            browser, Selector(select='[data-test="msg-markdown"]')
        )
        self.cancel_btn = Button(
            browser,
            Selector(
                by=By.XPATH, select='//span[@data-test="label" and text()="Cancel"]'
            ),
        )
        self.close_btn = Button(
            browser, Selector(select=container.select + ' button[data-test="close"]')
        )
        if self.add_btn == None:
            self.create_new_input = Dropdown(
                browser, Selector(by=By.ID, select="addInputBtn")
            )

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

    def is_error_closed(self):
        try:
            self.msg_error.get_msg()
            return False
        except:
            return True

    def save(
        self, expect_error: bool = False, expect_warning: bool = False
    ) -> Union[str, bool]:
        """
        Attempts to save configuration. If error or warning messages are found, return them instead.
        """
        warnings.warn(
            "expect_error and expect_warning are deprecated and will be removed in the future versions.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.save_btn.wait_to_be_clickable()
        self.save_btn.click()
        try:
            error_message = self.get_error()
        except selenium.common.exceptions.TimeoutException:
            error_message = ""
        if error_message != "":
            return error_message
        try:
            warning_message = self.get_warning()
        except selenium.common.exceptions.TimeoutException:
            warning_message = ""
        if warning_message != "":
            return warning_message
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
