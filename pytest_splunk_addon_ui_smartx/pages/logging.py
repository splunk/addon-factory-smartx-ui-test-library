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

import time

from selenium.webdriver.common.by import By

from ..backend_confs import SingleBackendConf
from ..components.base_component import Selector
from ..components.controls.single_select import SingleSelect
from ..components.entity import Entity
from ..components.tabs import Tab


class Logging(Entity):
    def __init__(
        self,
        ta_name,
        ta_conf="",
        ucc_smartx_selenium_helper=None,
        ucc_smartx_rest_helper=None,
    ):
        """
        :param ta_name: Name of TA
        :param ta_conf: Name of conf file
        :param ucc_smartx_selenium_helper: Fixture with selenium driver, urls(web, mgmt) and session key
        :param ucc_smartx_rest_helper: Fixture with selenium driver, urls(mgmt)
        """
        entity_container = Selector(select='div[id="loggingTab"]')
        self.ta_name = ta_name
        self.ta_conf = ta_conf
        if self.ta_conf == "":
            self.ta_conf = "{}_settings".format(self.ta_name.lower())

        if ucc_smartx_selenium_helper:
            super().__init__(ucc_smartx_selenium_helper.browser, entity_container)
            self.splunk_web_url = ucc_smartx_selenium_helper.splunk_web_url
            self.log_level = SingleSelect(
                ucc_smartx_selenium_helper.browser,
                Selector(select='[data-test="control-group"][data-name="loglevel"]'),
            )
            self.open()
        if ucc_smartx_rest_helper:
            self.splunk_mgmt_url = ucc_smartx_rest_helper.splunk_mgmt_url
            self.backend_conf = SingleBackendConf(
                self._get_logging_url(),
                ucc_smartx_rest_helper.username,
                ucc_smartx_rest_helper.password,
            )

    def open(self):
        """
        Open the required page. Page(super) class opens the page by default.
        """
        self.browser.get(
            "{}/en-US/app/{}/configuration".format(self.splunk_web_url, self.ta_name)
        )
        tab = Tab(self.browser)
        tab.open_tab("logging")

    def _get_logging_url(self):
        """
        get rest endpoint for the configuration
            :returns: str endpoint for the configuration file
        """
        return "{}/servicesNS/nobody/{}/configs/conf-{}/logging".format(
            self.splunk_mgmt_url, self.ta_name, self.ta_conf
        )
