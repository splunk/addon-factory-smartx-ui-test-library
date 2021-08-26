# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from .base_component import BaseComponent, Selector
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class Popup(BaseComponent):
    """
    Component: Popup
    To clear Popups in the Splunk instance
    """
    def __init__(self, browser, container=Selector(select= """ button[label="Don't show me this again"]""")):
        """
            :param browser: The selenium webdriver
        """
        super(Popup, self).__init__(browser, container)

    def pop(self):
        """
        Disable the popup within Splunk
        """
        try: 
            self.wait_for("container")
            self.container.click()
        except TimeoutException:
            pass