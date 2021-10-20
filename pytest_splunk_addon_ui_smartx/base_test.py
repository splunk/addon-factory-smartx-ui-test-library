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

import logging
import os
import re
import sys
import time
import traceback

import pytest
import requests
from msedge.selenium_tools import Edge, EdgeOptions
from msedge.selenium_tools.remote_connection import EdgeRemoteConnection
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
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

    sauce_username = None
    sauce_access_key = None
    sauce_tunnel_id = None
    sauce_tunnel_parent = None
    jenkins_build = None

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
        self.skip_saucelab_job = False

        if "grid" in browser:
            self.skip_saucelab_job = True
            debug = True

        if not debug:
            # Using Saucelabs
            self.init_sauce_env_variables()

        try:
            if browser == "firefox":
                if debug:
                    self.browser = webdriver.Firefox(
                        firefox_options=self.get_local_firefox_opts(headless),
                        log_path="selenium.log",
                    )
                else:
                    self.browser = webdriver.Remote(
                        command_executor="https://ondemand.saucelabs.com:443/wd/hub",
                        desired_capabilities=self.get_sauce_firefox_opts(
                            browser_version
                        ),
                    )

            elif browser == "chrome":
                if debug:
                    self.browser = webdriver.Chrome(
                        chrome_options=self.get_local_chrome_opts(headless),
                        service_args=["--verbose", "--log-path=selenium.log"],
                    )
                else:
                    self.browser = webdriver.Remote(
                        command_executor="https://ondemand.saucelabs.com:443/wd/hub",
                        desired_capabilities=self.get_sauce_chrome_opts(
                            browser_version
                        ),
                    )

            # selenium local stack
            elif browser == "chrome_grid":
                google_cert_opts = {
                    "goog:chromeOptions": {
                        "w3c": True,
                        "args": ["ignore-certificate-errors", "ignore-ssl-errors=yes"],
                    }
                }

                self.browser = webdriver.Remote(
                    command_executor="http://chrome-grid:4444/wd/hub",
                    desired_capabilities=self.get_grid_opts("chrome", google_cert_opts),
                )
            elif browser == "firefox_grid":
                firefox_cert_opts = {
                    "acceptInsecureCerts": True,
                    "acceptSslCerts": True,
                }

                self.browser = webdriver.Remote(
                    command_executor="http://firefox-grid:4444/wd/hub",
                    desired_capabilities=self.get_grid_opts(
                        "firefox", firefox_cert_opts
                    ),
                )
            # kubernetes selenium
            elif browser == "chrome_k8s":
                google_cert_opts = {
                    "goog:chromeOptions": {
                        "w3c": True,
                        "args": ["ignore-certificate-errors", "ignore-ssl-errors=yes"],
                    }
                }

                self.browser = webdriver.Remote(
                    command_executor="http://selenium-hub.selenium.svc.cluster.local:4444/wd/hub",
                    desired_capabilities=self.get_grid_opts("chrome", google_cert_opts),
                )
            elif browser == "firefox_k8s":
                firefox_cert_opts = {
                    "acceptInsecureCerts": True,
                    "acceptSslCerts": True,
                }

                self.browser = webdriver.Remote(
                    command_executor="http://selenium-hub.selenium.svc.cluster.local:4444/wd/hub",
                    desired_capabilities=self.get_grid_opts(
                        "firefox", firefox_cert_opts
                    ),
                )

            elif browser == "edge":
                if debug:
                    self.browser = Edge(
                        executable_path="msedgedriver",
                        desired_capabilities=self.get_local_edge_opts(headless),
                        service_args=["--verbose", "--log-path=selenium.log"],
                    )
                else:
                    command_executor = EdgeRemoteConnection(
                        "https://ondemand.saucelabs.com:443/wd/hub"
                    )
                    options = EdgeOptions()
                    options.use_chromium = True
                    self.browser = webdriver.Remote(
                        command_executor=command_executor,
                        options=options,
                        desired_capabilities=self.get_sauce_edge_opts(browser_version),
                    )

            elif browser == "IE":
                if debug:
                    self.browser = webdriver.Ie(capabilities=self.get_local_ie_opts())
                else:
                    self.browser = webdriver.Remote(
                        command_executor="https://ondemand.saucelabs.com:443/wd/hub",
                        desired_capabilities=self.get_sauce_ie_opts(browser_version),
                    )
            elif browser == "safari":
                if debug:
                    self.browser = webdriver.Safari()
                else:
                    self.browser = webdriver.Remote(
                        command_executor="https://ondemand.saucelabs.com:443/wd/hub",
                        desired_capabilities=self.get_sauce_safari_opts(
                            browser_version
                        ),
                    )
            else:
                raise Exception(
                    "No valid browser found.! expected=[firefox, chrome, safari], got={}".format(
                        browser
                    )
                )
        except Exception as e:
            raise e

        try:
            self.browser_session = self.browser.session_id
            self.login_to_splunk(*self.cred)
        except:
            self.browser.quit()
            if not debug:
                self.update_saucelab_job(False)
            raise

    @classmethod
    def init_sauce_env_variables(cls):
        # Read Environment variables to fetch saucelab credentials
        if cls.sauce_username and cls.sauce_access_key:
            return
        cls.sauce_username = os.environ.get("SAUCE_USERNAME")
        cls.sauce_access_key = os.environ.get("SAUCE_PASSWORD")
        cls.sauce_tunnel_id = os.environ.get("SAUCE_TUNNEL_ID") or "sauce-ha-tunnel"
        cls.sauce_tunnel_parent = os.environ.get("SAUCE_TUNNEL_PARENT") or "qtidev"
        if cls.sauce_tunnel_parent in ["null", "none"]:
            cls.sauce_tunnel_parent = None

        cls.jenkins_build = (
            os.environ.get("JOB_NAME")
            or os.environ.get("JENKINS_JOB_ID")
            or "Local Run"
        )
        print("\nUsing Saucelabs tunnel: {}".format(cls.sauce_tunnel_id))
        if not cls.sauce_username or not cls.sauce_access_key:
            raise Exception(
                "SauceLabs Credentials not found in the environment."
                " Please make sure SAUCE_USERNAME and SAUCE_PASSWORD is set."
            )

    def get_grid_opts(self, browser, custom_browser_options):
        return {
            "browserName": browser,
            "platformName": "linux",
            "se:recordVideo": "true",
            "se:timeZone": "US/Pacific",
            "se:screenResolution": "1920x1080",
            **custom_browser_options,
        }

    def get_sauce_opts(self):
        # Get saucelab default options
        sauce_options = {
            "screenResolution": "1280x768",
            "seleniumVersion": "3.141.0",
            # best practices involve setting a build number for version control
            "build": self.jenkins_build,
            "name": self.test_case,
            "username": self.sauce_username,
            "accessKey": self.sauce_access_key,
            # setting sauce-runner specific parameters such as timeouts helps
            # manage test execution speed.
            "maxDuration": 1800,
            "commandTimeout": 300,
            "idleTimeout": 1000,
            "tunnelIdentifier": self.sauce_tunnel_id,
        }
        if self.sauce_tunnel_parent:
            sauce_options["parenttunnel"] = self.sauce_tunnel_parent

        return sauce_options

    def get_sauce_ie_opts(self, browser_version):
        sauce_options = {
            "build": self.jenkins_build,
            "name": self.test_case,
            "username": self.sauce_username,
            "accessKey": self.sauce_access_key,
            "tunnelIdentifier": "sauce-ha-tunnel",
            "parenttunnel": "qtidev",
            "platformName": "Windows 10",
            "browserName": "internet explorer",
            "seleniumVersion": "3.141.0",
            "iedriverVersion": "3.141.0",
            "maxDuration": 1800,
            "commandTimeout": 300,
            "idleTimeout": 1000,
        }
        ie_opts = {
            "platformName": "Windows 10",
            "browserName": "internet explorer",
            "browserversion": browser_version,
            "iedriverVersion": "3.141.0",
            "sauce:options": sauce_options,
        }
        return ie_opts

    def get_local_ie_opts(self):
        capabilities = DesiredCapabilities.INTERNETEXPLORER
        capabilities["se:ieOptions"] = {}
        capabilities["ignoreZoomSetting"] = True
        capabilities["se:ieOptions"]["ie.ensureCleanSession"] = True
        capabilities["requireWindowFocus"] = True
        capabilities["nativeEvent"] = False
        return capabilities

    def get_local_chrome_opts(self, headless_run):
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_argument("--ignore-ssl-errors=yes")
        chrome_opts.add_argument("--ignore-certificate-errors")
        if headless_run:
            chrome_opts.add_argument("--headless")
            chrome_opts.add_argument("--window-size=1280,768")
        return chrome_opts

    def get_local_firefox_opts(self, headless_run):
        firefox_opts = webdriver.FirefoxOptions()
        firefox_opts.log.level = "trace"
        if headless_run:
            firefox_opts.add_argument("--headless")
            firefox_opts.add_argument("--window-size=1280,768")
        return firefox_opts

    def get_local_edge_opts(self, headless_run):
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

    def get_sauce_firefox_opts(self, browser_version):
        firefox_opts = {
            "platformName": "Windows 10",
            "browserName": "firefox",
            "browserVersion": browser_version,
            "sauce:options": self.get_sauce_opts(),
            "acceptInsecureCerts": True,
            "acceptSslCerts": True,
        }
        return firefox_opts

    def get_sauce_edge_opts(self, browser_version):
        edge_opts = {
            "platformName": "Windows 10",
            "browserVersion": browser_version,
            "sauce:options": self.get_sauce_opts(),
            "acceptInsecureCerts": True,
            "acceptSslCerts": True,
        }
        return edge_opts

    def get_sauce_chrome_opts(self, browser_version):
        chrome_opts = {
            "platformName": "Windows 10",
            "browserName": "chrome",
            "browserVersion": browser_version,
            "goog:chromeOptions": {
                "w3c": True,
                "args": ["ignore-certificate-errors", "ignore-ssl-errors=yes"],
            },
            "sauce:options": self.get_sauce_opts(),
        }
        return chrome_opts

    def get_sauce_safari_opts(self, browser_version):
        try:
            retries = 0
            while retries < 3:
                response = requests.get(
                    "https://api.us-west-1.saucelabs.com/rest/v1/info/platforms/webdriver",
                    verify=False,
                )
                if response.status_code != 200:
                    logger.debug(
                        "Error retrieving supported webdrivers for saucelabs, retrying..."
                    )
                    logger.debug("Status Code: " + str(response.status_code))
                    logger.debug(response.text)
                    retries += 1
                    time.sleep(1 * 60)
                else:
                    break
            if response.status_code != 200:
                raise Exception(
                    "Error retrieving supported webdrivers for saucelabs\n Status: {}\nURL: {}".format(
                        response.status_code, response.url
                    )
                )
            safari_versions = {}
            for items in response.json():
                if items["api_name"] == "safari":
                    if items["short_version"] in safari_versions:
                        safari_versions[int(items["short_version"])] = max(
                            items["os"], safari_versions[items["short_version"]]
                        )
                    else:
                        safari_versions[int(items["short_version"])] = items["os"]
            if browser_version == "latest":
                browser_version = str(max(safari_versions.keys()))
                platformName = safari_versions[int(browser_version)]
            else:
                if int(browser_version) not in safari_versions:
                    raise Exception(
                        "Failed to obtain Safari version for saucelabs (Requested version: {})\nGot the following Safari versions={}".format(
                            browser_version, safari_versions
                        )
                    )
                else:
                    platformName = safari_versions[int(browser_version)]
        except ValueError:
            raise Exception(
                "Received an incorrect value for safari version (received{})\nSafari Version should be an int or the string 'latest'".format(
                    browser_version
                )
            )
        except Exception as e:
            logger.debug("Supported webdrivers for Saucelab: " + response.text)
            raise e
        sauce_opts = self.get_sauce_opts()
        sauce_opts["screenResolution"] = "1024x768"
        safari_opts = {
            "browserName": "safari",
            "platformName": platformName,
            "browserVersion": browser_version,
            "sauce:options": sauce_opts,
        }
        return safari_opts

    def login_to_splunk(self, *cred):
        try:
            login_page = LoginPage(self)
            login_page.login.login(*cred)
        except:
            self.browser.save_screenshot(os.path.join(PNG_PATH, "login_error.png"))
            raise

    def update_saucelab_job(self, status):
        if self.skip_saucelab_job:
            return
        data = '{"passed": false}' if status else '{"passed": true}'
        response = requests.put(
            "https://saucelabs.com/rest/v1/{}/jobs/{}".format(
                self.sauce_username, self.browser_session
            ),
            data=data,
            auth=(self.sauce_username, self.sauce_access_key),
        )
        response = response.json()
        print("\nSauceLabs job_id={}".format(response.get("id")))
        print("SauceLabs Video_url={}".format(response.get("video_url")))


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
        except:
            raise Exception(
                "Could not parse the content returned from Management Port. Recheck the mgmt url."
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
