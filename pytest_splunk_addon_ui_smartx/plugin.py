# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0
import os
import pytest
from filelock import FileLock
from collections import namedtuple
import traceback
import logging
from pytest_splunk_addon.splunk import ( 
    splunk, 
    splunk_docker, 
    splunk_external, 
    splunk_rest_uri, 
    splunk_web_uri, 
    is_responsive_splunk, 
    is_responsive 
) 

from .base_test import SeleniumHelper, RestHelper

LOGGER = logging.getLogger("pytest-ucc-smartx")
PNG_PATH = "assets"

def pytest_configure(config):
    """
    Setup configuration after command-line options are parsed
    """
    config.addinivalue_line(
        "markers", "ucc: UCC Tests"
    )
    pytest_html = config.pluginmanager.getplugin('html')
    if pytest_html:
        try:
            os.mkdir(PNG_PATH)
        except OSError:
            pass

def pytest_fixture_setup(fixturedef, request):
    """
    Setup configuration after command-line options are parsed
    """
    if fixturedef.argname == "ucc_smartx_selenium_helper" and request.config.getoption("--local") and request.config.getoption("--persist-browser"):
        fixturedef.scope = "session"

def pytest_addoption(parser):
    parser.conflict_handler = "resolve"
    group = parser.getgroup("splunk-ucc-smartx")
  
    group.addoption(
        "--browser", 
        action="store", 
        help=( "The browser on which the test should run. supported_values: (firefox, chrome, safari)." 
        " You can also provide browser version if the tests are running on Saucelabs. "
        "ex, <browser>:<version>. default version is latest. For safari, the default is version 12.")
    )

    group.addoption(
        "--local", 
        action="store_true", 
        help="The test will be run on local browsers"
    )

    group.addoption(
        "--persist-browser", 
        action="store_true", 
        help=(
            "For local execution, keep a single browser to executed all tests."
        )
    )

    group.addoption(
        "--setup-retry-count", 
        action="store_true", 
        default="1",
        help="The number of times the browser should try to connect to the SeleniumBrowser"
    )

    group.addoption(
        "--headless", 
        action="store_true", 
        help="Run the test case on headless mode"
    )

SmartConfigs = namedtuple("SmartConfigs", ['driver', 'driver_version', 'local_run', 'retry_count', 'headless_run'])

@pytest.fixture(scope="session")
def ucc_smartx_configs(request):

    if not request.config.getoption("--browser"):
        raise ValueError(
            "--browser parameter was not provided while running the test cases."
            )
    driver = request.config.getoption("--browser")
    LOGGER.debug("--browser={}".format(driver))
    if len(driver.split(':')) == 2:
        driver, driver_version = driver.split(':')
    else:
        if driver == 'safari':
            driver_version = '12'
        else:
            driver_version = "latest"
        
    if request.config.getoption("--local"):
        local_run = True
        LOGGER.debug("--debug")
    else:
        local_run = False

    if request.config.getoption("--setup-retry-count"):
        retry_count = int(request.config.getoption("--setup-retry-count"))
        LOGGER.debug("--setup-retry-count={}".format(retry_count))
    else:
        retry_count = 1

    if request.config.getoption("--headless"):
        headless_run = True
        LOGGER.debug("--headless")
    else:
        headless_run = False

    LOGGER.info("Calling SeleniumHelper with:: browser={driver}, debug={local_run}, headless={headless_run})".format(
        driver=driver, local_run=local_run, headless_run=headless_run
    ))
    smartx_configs = SmartConfigs(driver=driver, driver_version=driver_version, local_run=local_run, retry_count=retry_count, headless_run=headless_run)
    return smartx_configs

@pytest.fixture(scope="function")
def ucc_smartx_selenium_helper(request, ucc_smartx_configs, splunk, splunk_web_uri, splunk_rest_uri):
    # Try to configure selenium & Login to splunk instance
    test_case = "{}_{}".format(ucc_smartx_configs.driver, request.node.nodeid.split("::")[-1])
    for try_number in range(ucc_smartx_configs.retry_count):
        last_exc = Exception()
        try:
            selenium_helper = SeleniumHelper(ucc_smartx_configs.driver, ucc_smartx_configs.driver_version, splunk_web_uri, splunk_rest_uri, debug=ucc_smartx_configs.local_run, cred=(splunk["username"], splunk["password"]), headless=ucc_smartx_configs.headless_run, test_case=test_case)
            request.node.selenium_helper = selenium_helper
            break
        except Exception as e:
            last_exc = e
            LOGGER.warn("Failed to configure the browser or login to Splunk instance for - Try={} \nTRACEBACK::{}".format(try_number, traceback.format_exc()))
    else:
        LOGGER.error("Could not connect to Browser or login to Splunk instance. Please check the logs for detailed error of each retry")
        raise(last_exc)

    def fin():
        LOGGER.info("Quiting browser..")
        selenium_helper.browser.quit()

        if not ucc_smartx_configs.local_run:
            LOGGER.debug("Notifying the status of the testcase to SauceLabs...")
            try:
                if hasattr(request.node, 'report'):
                    selenium_helper.update_saucelab_job(request.node.report.failed)
                else:
                    LOGGER.info("Could not notify to sauce labs because scope of fixture is not set to function")
            except:
                LOGGER.warn("Could not notify to Saucelabs \nTRACEBACK::{}".format(traceback.format_exc()))

    request.addfinalizer(fin)
    return selenium_helper

@pytest.fixture(scope="session")
def ucc_smartx_rest_helper(ucc_smartx_configs, splunk, splunk_rest_uri):
    # Try to configure rest endpoint
    splunk_rest_session, splunk_rest_uri = splunk_rest_uri
    for try_number in range(ucc_smartx_configs.retry_count):
        last_exc = Exception()
        try:
            rest_helper = RestHelper(splunk_rest_uri, splunk["username"], splunk["password"])
            break
        except Exception as e:
            last_exc = e
            LOGGER.warn("Failed to configure rest endpint for Splunk instance - Try={} \nTRACEBACK::{}".format(try_number, traceback.format_exc()))
    else:
        LOGGER.error("Could not connect to Splunk instance. Please check the logs for detailed error of each retry")
        raise(last_exc)
    return rest_helper


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """
    pytest_runtest_makereport will be called after each test case is executed.
    Capture a screenshot if the test case is failed.
    item.selenium_helper has been added by the fixture "test_helper". The scope of the fixture must be function.
        :param item: the method of the test case.
    """
    LOGGER.debug("pytest_runtest_makereport: Start making report")
    try:
        pytest_html = item.config.pluginmanager.getplugin('html')
        if pytest_html:
            outcome = yield
            report = outcome.get_result()
            if report.when == "call" or report.when == "setup":
                setattr(item, 'report', report)
                if report.failed:
                    try:
                        if report.when == "setup":
                            # Possible - Login failed
                            # the item will not have selenium_helper
                            screenshot_path = os.path.join(PNG_PATH, "login_error.png")
                        else:
                            # Test Failed
                            screenshot_path = os.path.join(PNG_PATH, item.nodeid.split("::")[-1] + ".png")
                            item.selenium_helper.browser.save_screenshot(screenshot_path)

                        report.extra = [pytest_html.extras.image(screenshot_path)]
                    except:
                        LOGGER.warn("Screenshot can not be captured. Scope of the fixture test_helper must be 'function' to capture the screenshot. ")
        else:
            LOGGER.warn("pytest-html is not installed. Install by using: pip install pytest-html")
    except Exception as e:
        LOGGER.warn("Got exception while making test report. Exception  {}".format(e))
        LOGGER.debug("test_report, Exception: {}".format(traceback.format_exc()))
