#
# Copyright 2024 Splunk Inc.
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
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from .base_component import BaseComponent, Selector

ENTERPRISE_CLOUD_ToS = True


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
        super().__init__(browser, container)

        self.elements = {
            "username": Selector(by=By.ID, select="username"),
            "password": Selector(by=By.ID, select="password"),
            "homepage": Selector(select='a[data-action="home"]'),
        }

    def login(self, username, password):
        """
        Login into the Splunk instance
            :param username: Str the username for the splunk instance we want to access
            :param password: Str the password for the splunk instance we want to access
        """
        self.username.send_keys(username)
        self.password.send_keys(password)
        self.password.send_keys("\ue007")
        self.wait_for("homepage", "Could not log in to the Splunk instance.")
