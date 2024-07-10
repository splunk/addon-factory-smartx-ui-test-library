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

import logging
import os
import sys

import requests
from msedge.selenium_tools import Edge
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait

from .pages.login import LoginPage
from .utils import backend_retry

# requests.urllib3.disable_warnings()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
PNG_PATH = "assets"


class SeleniumHelper:
    """
    The helper class provides the Remote Browser
    """

    def __init__(
        self,
        browser,
        browser_version,
        splunk_web_url,
        splunk_mgmt_url,
        debug=False,
        cred=("admin", "Chang3d!"),
        headless=False,
        test_case=None,
    ):
        self.splunk_web_url = splunk_web_url
        self.splunk_mgmt_url = splunk_mgmt_url
        self.cred = cred
        self.test_case = test_case

        selenium_host = os.environ.get("SELENIUM_HOST")

        try:
            if browser == "firefox":
                if debug:
                    self.browser = webdriver.Firefox(
                        firefox_options=SeleniumHelper.get_local_firefox_opts(headless)
                    )
                elif selenium_host:
                    self.browser = webdriver.Remote(
                        command_executor=f"{selenium_host}:4444/wd/hub",
                        options=SeleniumHelper.get_local_firefox_opts(
                            headless_run=False
                        ),
                    )
                    self.browser.implicitly_wait(3)
                else:
                    raise Exception(
                        f"Firefox tests have to be run either with --local or in CI environment with selenium host!"
                    )

            elif browser == "chrome":
                if debug:
                    self.browser = webdriver.Chrome(
                        chrome_options=SeleniumHelper.get_local_chrome_opts(headless),
                        service_args=["--verbose"],
                    )
                elif selenium_host:
                    self.browser = webdriver.Remote(
                        command_executor=f"{selenium_host}:4444/wd/hub",
                        options=SeleniumHelper.get_local_chrome_opts(
                            headless_run=False
                        ),
                    )
                    self.browser.implicitly_wait(3)
                else:
                    raise Exception(
                        f"Chrome tests have to be run either with --local or in CI environment with selenium host!"
                    )
            elif browser == "edge":
                if debug:
                    self.browser = Edge(
                        executable_path="msedgedriver",
                        desired_capabilities=SeleniumHelper.get_local_edge_opts(
                            headless
                        ),
                        service_args=["--verbose"],
                    )
                else:
                    raise Exception(
                        f"Edge tests are available only with --local option"
                    )
            elif browser == "IE":
                if debug:
                    self.browser = webdriver.Ie(
                        capabilities=SeleniumHelper.get_local_ie_opts()
                    )
                else:
                    raise Exception(f"IE tests are available only with --local option")
            elif browser == "safari":
                if debug:
                    self.browser = webdriver.Safari()
                else:
                    raise Exception(
                        f"Safari tests are available only with --local option"
                    )
            else:
                raise Exception(
                    f"No valid browser found.! expected=[firefox, chrome, edge, IE, safari], got={browser}"
                )
        except Exception as e:
            raise e

        try:
            self.browser_session = self.browser.session_id
            self.login_to_splunk(*self.cred)
        except Exception as e:
            self.browser.quit()
            logger.error(
                f"An unexpected error occurred during SeleniumHelper initialization: {e})"
            )
            raise

    @staticmethod
    def get_local_ie_opts():
        capabilities = DesiredCapabilities.INTERNETEXPLORER
        capabilities["se:ieOptions"] = {}
        capabilities["ignoreZoomSetting"] = True
        capabilities["se:ieOptions"]["ie.ensureCleanSession"] = True
        capabilities["requireWindowFocus"] = True
        capabilities["nativeEvent"] = False
        return capabilities

    @staticmethod
    def get_local_chrome_opts(headless_run):
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_argument("--ignore-ssl-errors=yes")
        chrome_opts.add_argument("--ignore-certificate-errors")
        chrome_opts.add_argument("--disable-dev-shm-usage")
        chrome_opts.add_argument("--window-size=1280,768")
        if headless_run:
            chrome_opts.add_argument("--headless")
        return chrome_opts

    @staticmethod
    def get_local_firefox_opts(headless_run):
        firefox_opts = webdriver.FirefoxOptions()
        firefox_opts.add_argument("--ignore-ssl-errors=yes")
        firefox_opts.add_argument("--ignore-certificate-errors")
        firefox_opts.add_argument("--disable-dev-shm-usage")
        firefox_opts.log.level = "trace"
        if headless_run:
            firefox_opts.add_argument("--headless")
            firefox_opts.add_argument("--window-size=1280,768")
        return firefox_opts

    @staticmethod
    def get_local_edge_opts(headless_run):
        if sys.platform.startswith("darwin"):
            platform = "MAC"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            platform = "WINDOWS"
        else:
            platform = "LINUX"
        DesiredCapabilities = {
            "platform": platform,
            "browserName": "MicrosoftEdge",
            "ms:edgeOptions": {
                "extensions": [],
                "args": ["--ignore-ssl-errors=yes", "--ignore-certificate-errors"],
            },
            "ms:edgeChromium": True,
        }
        if headless_run:
            DesiredCapabilities["ms:edgeOptions"]["args"].append("--headless")
            DesiredCapabilities["ms:edgeOptions"]["args"].append(
                "--window-size=1280,768"
            )
        return DesiredCapabilities

    def login_to_splunk(self, *cred):
        try:
            login_page = LoginPage(self)
            login_page.login.login(*cred)
        except Exception as e:
            logger.error(
                f"An unexpected error error occurred while logging to splunk: {e}"
            )
            self.browser.save_screenshot(os.path.join(PNG_PATH, "login_error.png"))
            raise


class RestHelper:
    def __init__(self, splunk_mgmt_url, username, password):
        self.splunk_mgmt_url = splunk_mgmt_url
        self.username = username
        self.password = password
        self.start_session()

    @backend_retry(3)
    def start_session(self):
        res = requests.post(
            self.splunk_mgmt_url + "/services/auth/login?output_mode=json",
            data={"username": self.username, "password": self.password},
            verify=False,
        )

        try:
            res = res.json()
        except Exception as e:
            raise Exception(
                f"Could not parse the content returned from Management Port. Recheck the mgmt url. Exception: {e}"
            )
        if (len(res.get("messages", [])) > 0) and (
            res["messages"][0].get("type") == "WARN"
        ):
            raise Exception(
                "Could not connect to the Splunk instance, verify credentials"
            )

        self.session_key = str(res["sessionKey"])


class UccTester:
    """
    The default setup and teardown methods can be added here.
    Use in case if some additional configuration should be added to all the test cases
    """

    def setup_class(self):
        WAIT_TIMEOUT = 20
        self.wait = WebDriverWait(None, WAIT_TIMEOUT)

    def assert_util(
        self, left, right, operator="==", left_args={}, right_args={}, msg=None
    ):
        """
        Try to check the condition for {WAIT_TIMEOUT} seconds.
        In UI Automation, it is not possible to expect things to work properly just milliseconds after an action.
        Even in manual testing, we try things after 4-5 seconds and 2-3 times.
        This utility method tries to achive the same assertion.
        To perform certain action multiple time, provide callable functoins with arguments.

        Params:
            left (object or callable): LHS of the operator.
            right (object or callable): RHS of the operator
            operator: Operator. Possible values: (==, !=, <, >, <=, >=, in, not in, is, is not)
            left_args: If left is callable, pass the parameters of the callable function.
            right_args: If right is callable, pass the parameters of the callable function.
            msg: Error message if the condition was not matched even after trying for {WAIT_TIMEOUT} seconds.

        """
        args = {
            "left": left,
            "right": right,
            "operator": operator,
            "left_args": left_args,
            "right_args": right_args,
            "left_value": left,
            "right_value": right,
        }
        operator_map = {
            "==": lambda left, right: left == right,
            "!=": lambda left, right: left != right,
            "<": lambda left, right: left < right,
            "<=": lambda left, right: left <= right,
            ">": lambda left, right: left > right,
            ">=": lambda left, right: left >= right,
            "in": lambda left, right: left in right,
            "not in": lambda left, right: left not in right,
            "is": lambda left, right: left is right,
            "is not": lambda left, right: left is not right,
        }

        def _assert(browser):
            try:
                if callable(args["left"]):
                    args["left_value"] = args["left"](**args["left_args"])
                if callable(args["right"]):
                    args["right_value"] = args["right"](**args["right_args"])
            except TimeoutException as e:
                raise Exception("Timeout: {}".format(str(e)))
            except ElementNotInteractableException as e:
                raise Exception("Element not interactable: {}".format(str(e)))
            return operator_map[args["operator"]](
                args["left_value"], args["right_value"]
            )

        try:
            self.wait.until(_assert)
            condition_failed = False
        except (TimeoutException, ElementNotInteractableException) as e:
            logger.error("Exception raised: {}".format(str(e)))
            condition_failed = True
        if condition_failed:
            if not msg:
                msg = "Condition Failed. \nLeft-value: {}\nOperator: {}\nRight-value: {}".format(
                    args["left_value"], args["operator"], args["right_value"]
                )
            assert operator_map[args["operator"]](
                args["left_value"], args["right_value"]
            ), msg
