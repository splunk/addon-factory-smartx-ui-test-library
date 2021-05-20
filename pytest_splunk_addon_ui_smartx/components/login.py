# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
import time
from .base_component import BaseComponent, Selector
from selenium.webdriver.common.by import By

SPLUNK_CLOUD_TOS = True
class Login(BaseComponent):
    """
    Component: Login
    To login into the Splunk instance
    """
    def __init__(self, browser, container=Selector(select="form.loginForm")):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
        """
        super(Login, self).__init__(browser, container)

        self.elements = {
            "username": Selector(by=By.ID, select="username"),
            "password": Selector(by=By.ID, select="password"),
            "homepage": Selector(select='a[data-action="home"]'),
            "accept_checkbox": Selector(by=By.ID, select="accept"),
            "accept_button": Selector(select=" .accept-tos-button.btn.btn-primary")
        }

    def login(self, username, password, splunk_cloud_agreement):
        """
        Login into the Splunk instance
            :param username: Str the username for the splunk instance we want to access
            :param password: Str the password for the splunk instance we want to access
        """
        global SPLUNK_CLOUD_TOS
        self.username.send_keys(username)
        self.password.send_keys(password)
        self.password.send_keys(u'\ue007')

        if splunk_cloud_agreement and SPLUNK_CLOUD_TOS:
            self.wait_to_be_clickable("accept_checkbox")
            self.accept_checkbox.click()
            self.wait_for("accept_button")
            self.accept_button.click()
            SPLUNK_CLOUD_TOS = False
        self.wait_for("homepage", "Could not log in to the Splunk instance.")
