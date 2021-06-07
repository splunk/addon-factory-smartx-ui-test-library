# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

import time
from selenium.webdriver.common.by import By

from ..backend_confs import SingleBackendConf
from ..components.entity import Entity
from .components.alert_base_component import Selector

from .components.button import Button
from .components.textbox import AlertTextBox
from .components.searchbox import SearchBox
from .components.dropdown import ActionDropdown

class ActionEntity(Entity):
    def __init__(self, browser):
        super(ActionEntity, self).__init__(browser, Selector(select=".trigger-actions-controls"))

class AlertEntity(Entity):

    def __init__(self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper):
        """
            :param ucc_smartx_configs: Fixture with selenium driver, urls(web, mgmt) and session key
            :param ta_name: Name of TA
            :param ta_conf: Name of conf file
        """
        entity_container = Selector(select=".main-section-body")
        if ucc_smartx_selenium_helper:
            super(AlertEntity, self).__init__(ucc_smartx_selenium_helper.browser, entity_container)
            self.splunk_web_url = ucc_smartx_selenium_helper.splunk_web_url

            # Controls 
            self.name = AlertTextBox(ucc_smartx_selenium_helper.browser, Selector(select="div[data-name=name]"))
            self.description = AlertTextBox(ucc_smartx_selenium_helper.browser, Selector(select="div[data-name=description]"))
            self.search = SearchBox(ucc_smartx_selenium_helper.browser, Selector(select=".search-bar-input"))
            self.add_action_dropdown = ActionDropdown(ucc_smartx_selenium_helper.browser, Selector(select=".add-action-btn"))
            self.add_alert = Button(ucc_smartx_selenium_helper.browser, Selector(select=".new-alert-button"))
            self.save_btn = Button(ucc_smartx_selenium_helper.browser, Selector(select=".alert-save-as .btn-save"))
            self.cancel_btn = Button(ucc_smartx_selenium_helper.browser, Selector(select=".alert-save-as .btn.cancel"))

    def open(self):
        """
        Open the required page. Page(super) class opens the page by default.
        """
        self.add_alert.click()
