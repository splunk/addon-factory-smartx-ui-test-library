import pytest
from filelock import FileLock
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

from .base_test import SeleniumHelper

LOGGER = logging.getLogger("pytest-ucc-smartx")

def pytest_configure(config):
    """
    Setup configuration after command-line options are parsed
    """
    config.addinivalue_line(
        "markers", "ucc: UCC Tests"
    )

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




# Fixture
@pytest.fixture(scope="session")
def ucc_smartx_configs(request, splunk, splunk_web_uri, splunk_rest_uri):
    # Configure pytest parameters, if provided

    if request.config.getoption("--browser"):
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

    test_case = driver + "_" + request.node.nodeid.split("::")[-1]
    splunk_rest_session, splunk_rest_uri = splunk_rest_uri

    LOGGER.info("Calling SeleniumHelper for test_case={test_case} with:: browser={driver}, web_url={web_url}, mgmt_url={mgmt_url}, debug={local_run}, cred=({username},{password}, headless={headless_run})".format(
        driver=driver, web_url=splunk_web_uri, mgmt_url=splunk_rest_uri, local_run=local_run, username=splunk["username"], password=splunk["password"], headless_run=headless_run, test_case=test_case
    ))

    # 3 Try to configure selenium & Login to splunk instance
    for try_number in range(retry_count):
        last_exc = Exception()
        try:
            helper = SeleniumHelper(driver, driver_version, splunk_web_uri, splunk_rest_uri, debug=local_run, cred=(splunk["username"], splunk["password"]), headless=headless_run, test_case=test_case)
            request.node.selenium_helper = helper
            break
        except Exception as e:
            last_exc = e
            LOGGER.warn("Failed to configure the browser or login to Splunk instance for - Try={} \nTRACEBACK::{}".format(try_number, traceback.format_exc()))
    else:
        LOGGER.error("Could not connect to Browser or login to Splunk instance. Please check the logs for detailed error of each retry")
        raise(last_exc)

    def fin():
        LOGGER.info("Quiting browser..")
        helper.browser.quit()

        if not local_run:
            LOGGER.debug("Notifying the status of the testcase to SauceLabs...")
            try:
                if hasattr(request.node, 'report'):
                    helper.update_saucelab_job(request.node.report.failed)
                else:
                    LOGGER.info("Could not notify to sauce labs because scope of fixture is not set to function")
            except:
                LOGGER.warn("Could not notify to Saucelabs \nTRACEBACK::{}".format(traceback.format_exc()))

    request.addfinalizer(fin)
    return helper
