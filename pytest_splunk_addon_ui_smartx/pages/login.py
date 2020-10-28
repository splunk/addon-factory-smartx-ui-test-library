# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from .page import Page
from ..components.login import Login
from selenium.webdriver.common.by import By

class LoginPage(Page):
    """
    Page: Login page
    """
    def __init__(self, ucc_smartx_selenium_helper):
        """
        :param ucc_smartx_selenium_helper: Fixture with selenium driver, urls(web, mgmt) and session key
        """

        super(LoginPage, self).__init__(ucc_smartx_selenium_helper, ucc_smartx_rest_helper=None)
        self.login = Login(ucc_smartx_selenium_helper.browser)
