#
# Copyright 2021 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


class Page:
    """
    Instance of a Page class holds all the components inside the page. To access the component, just do page.component.action_method()
    The page class should not have any interaction method for any visible components. It is supposed to hold all the components only.
    """

    def __init__(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, open_page=True
    ):
        """
        :param ucc_smartx_selenium_helper: The selenium webdriver
        :param ucc_smartx_rest_helper: Splunk web & management url. {"web": , "mgmt": }
        """
        if ucc_smartx_selenium_helper:
            self.browser = ucc_smartx_selenium_helper.browser
            self.splunk_web_url = ucc_smartx_selenium_helper.splunk_web_url
            if open_page:
                self.open()
        if ucc_smartx_rest_helper:
            self.splunk_mgmt_url = ucc_smartx_rest_helper.splunk_mgmt_url

    def open(self):
        """
        Abstract Method. Open the page
        """
        self.browser.get(self.splunk_web_url)
