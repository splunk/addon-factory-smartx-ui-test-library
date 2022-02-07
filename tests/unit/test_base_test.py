import importlib
from copy import deepcopy
from unittest.mock import ANY, MagicMock, patch

import pytest
import selenium
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException

import pytest_splunk_addon_ui_smartx.base_test
from pytest_splunk_addon_ui_smartx.base_test import (
    RestHelper,
    SeleniumHelper,
    UccTester,
)

SAUCE_OPTIONS = {
    "screenResolution": "1280x768",
    "seleniumVersion": "3.141.0",
    "build": "JOB_NAME",
    "name": None,
    "username": "SAUCE_USERNAME",
    "accessKey": "SAUCE_PASSWORD",
    "maxDuration": 1800,
    "commandTimeout": 300,
    "idleTimeout": 1000,
    "tunnelIdentifier": "SAUCE_TUNNEL_ID",
    "parenttunnel": "SAUCE_TUNNEL_PARENT",
}


def test_exception_when_config_sauce_env_missing():
    importlib.reload(pytest_splunk_addon_ui_smartx.base_test)
    with patch("os.environ.get", return_value=""):
        with pytest.raises(Exception):
            pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.init_sauce_env_variables()


@pytest.mark.parametrize(
    "test_input,expected", [("tunnel", "tunnel"), ("null", None), ("none", None)]
)
def test_sauce_tunnel_parent(test_input, expected):
    importlib.reload(pytest_splunk_addon_ui_smartx.base_test)
    with patch("os.environ.get", return_value=test_input):
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.init_sauce_env_variables()
    assert (
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.sauce_tunnel_parent
        == expected
    )


def test_init_sauce_env_set_config_once():
    with patch("os.environ.get", return_value="B"):
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.sauce_username = "A"
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.sauce_access_key = "A"
    assert (
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.init_sauce_env_variables()
        is None
    )
    assert pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.sauce_username == "A"
    assert (
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.sauce_access_key == "A"
    )


def test_init_sauce_env_set_qtidev_when_sauce_tunnel_parent_is_missing():
    importlib.reload(pytest_splunk_addon_ui_smartx.base_test)
    with patch("os.environ.get", lambda x: {"SAUCE_TUNNEL_PARENT": ""}.get(x, x)):
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.init_sauce_env_variables()
    assert (
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper.sauce_tunnel_parent
        == "qtidev"
    )


default_args_for_selenium_helper = {
    "browser": "chrome",
    "browser_version": "88",
    "splunk_web_url": "https://localhost:8000",
    "splunk_mgmt_url": "https://localhost:8089",
    "debug": True,
    "cred": ("admin", "Chang3d!"),
    "headless": False,
    "test_case": None,
}


def test_selenium_helper_raise_exception_with_given_invalid_browser_version():
    with pytest.raises(Exception, match="No valid browser found.") as e:
        SeleniumHelper(**{**default_args_for_selenium_helper, "browser": "aa"})


@pytest.mark.parametrize("debug", [True, False])
@pytest.mark.parametrize(
    "browser,webdriver",
    [
        ("firefox", "selenium.webdriver.Firefox"),
        ("chrome", "selenium.webdriver.Chrome"),
        ("IE", "selenium.webdriver.Ie"),
        ("safari", "selenium.webdriver.Safari"),
        ("edge", "pytest_splunk_addon_ui_smartx.base_test.Edge"),
    ],
)
def test_constructor_selenium_helper(browser, webdriver, debug):
    with patch(webdriver if debug else "selenium.webdriver.Remote"), patch(
        "os.environ.get", lambda x: x
    ):
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper(
            **{
                **default_args_for_selenium_helper,
                "browser": browser,
                "debug": debug,
                "browser_version": 11,
            }
        )


@pytest.mark.parametrize(
    "browser,expected_config",
    [
        (
            "edge",
            {
                "platformName": ANY,
                "browserVersion": 11,
                "sauce:options": SAUCE_OPTIONS,
                "acceptInsecureCerts": True,
                "acceptSslCerts": True,
            },
        ),
        (
            "IE",
            {
                "platformName": ANY,
                "browserName": "internet explorer",
                "browserversion": 11,
                "iedriverVersion": "3.141.0",
                "sauce:options": SAUCE_OPTIONS,
            },
        ),
        (
            "firefox",
            {
                "platformName": ANY,
                "browserName": "firefox",
                "browserVersion": 11,
                "sauce:options": SAUCE_OPTIONS,
                "acceptInsecureCerts": True,
                "acceptSslCerts": True,
            },
        ),
        (
            "chrome",
            {
                "platformName": ANY,
                "browserName": "chrome",
                "browserVersion": 11,
                "goog:chromeOptions": {
                    "w3c": True,
                    "args": ["ignore-certificate-errors", "ignore-ssl-errors=yes"],
                },
                "sauce:options": SAUCE_OPTIONS,
            },
        ),
        (
            "safari",
            {
                "browserName": "safari",
                "platformName": ANY,
                "browserVersion": 11,
                "sauce:options": SAUCE_OPTIONS,
            },
        ),
        (
            "chrome_grid",
            {
                "browserName": "chrome",
                "platformName": "linux",
                "se:recordVideo": "true",
                "se:timeZone": "US/Pacific",
                "se:screenResolution": "1920x1080",
                "goog:chromeOptions": {
                    "w3c": True,
                    "args": ["ignore-certificate-errors", "ignore-ssl-errors=yes"],
                },
            },
        ),
        (
            "firefox_grid",
            {
                "browserName": "firefox",
                "platformName": "linux",
                "se:recordVideo": "true",
                "se:timeZone": "US/Pacific",
                "se:screenResolution": "1920x1080",
                "acceptInsecureCerts": True,
                "acceptSslCerts": True,
            },
        ),
    ],
)
def test_desired_capabilities_for_saucelabs(browser, expected_config):
    importlib.reload(pytest_splunk_addon_ui_smartx.base_test)
    with patch("selenium.webdriver.Remote") as webdriver, patch(
        "os.environ.get", lambda x: x
    ):
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper(
            **{
                **default_args_for_selenium_helper,
                "browser": browser,
                "debug": False,
                "browser_version": 11,
            }
        )
    assert webdriver.call_args[1].get("desired_capabilities") == expected_config


def test_capabilities_for_firefox_local():
    with patch("selenium.webdriver.Firefox") as webdriver_, patch(
        "os.environ.get", lambda x: x
    ):
        selenium_helper = pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper
        selenium_helper.get_local_firefox_opts = MagicMock(return_value=f"firefox_opts")
        selenium_helper(
            **{
                **default_args_for_selenium_helper,
                "browser": "firefox",
            }
        )
        webdriver_.assert_called_with(
            firefox_options="firefox_opts", log_path="selenium.log"
        )
        selenium_helper.get_local_firefox_opts.assert_called_with(False)


def test_capabilities_for_chrome_local():
    with patch("selenium.webdriver.Chrome") as webdriver_, patch(
        "os.environ.get", lambda x: x
    ):
        selenium_helper = pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper
        selenium_helper.get_local_chrome_opts = MagicMock(return_value=f"chrome_opts")
        selenium_helper(
            **{
                **default_args_for_selenium_helper,
                "browser": "chrome",
            }
        )
        webdriver_.assert_called_with(
            chrome_options="chrome_opts",
            service_args=["--verbose", "--log-path=selenium.log"],
        )
        selenium_helper.get_local_chrome_opts.assert_called_with(False)


def test_capabilities_for_ie_local():
    with patch("selenium.webdriver.Ie") as webdriver_, patch(
        "os.environ.get", lambda x: x
    ):
        selenium_helper = pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper
        selenium_helper.get_local_ie_opts = MagicMock(return_value=f"ie_opts")
        selenium_helper(
            **{
                **default_args_for_selenium_helper,
                "browser": "IE",
            }
        )
        webdriver_.assert_called_with(capabilities="ie_opts")
        selenium_helper.get_local_ie_opts.assert_called_once()


@pytest.fixture()
def ucc_mock():
    ucc = UccTester()
    ucc.wait = MagicMock()

    def f(x):
        out = x("fake_browser")
        if out:
            return out
        raise TimeoutException

    ucc.wait.until.side_effect = f
    return ucc


@pytest.mark.parametrize(
    "left, right, operator",
    [
        (lambda x: x, lambda x: x, "=="),
        (lambda x: x, lambda x: not x, "!="),
        (lambda x: -x, lambda x: x, "<"),
        (lambda x: -x, lambda x: x, "<="),
        (lambda x: x, lambda x: x, "<="),
        (lambda x: x, lambda x: -x, ">"),
        (lambda x: x, lambda x: -x, ">="),
        (lambda x: x, lambda x: x, ">="),
        (lambda x: x, lambda x: [x, 1, 2], "in"),
        (lambda x: x, [], "not in"),
        (lambda x: x, lambda x: x, "is"),
        (lambda x: x, lambda x: not x, "is not"),
    ],
)
def test_operator_map_callable_obj_pass(ucc_mock, left, right, operator):
    args = {"x": 1}
    ucc_mock.assert_util(left, right, operator, args, args)


@pytest.mark.parametrize(
    "left, right, operator",
    [
        (lambda x: x, lambda x: -x, "=="),
        (lambda x: x, lambda x: x, "!="),
        (lambda x: x, lambda x: x, "<"),
        (lambda x: x, lambda x: -x, "<"),
        (lambda x: x, lambda x: -x, "<="),
        (lambda x: x, lambda x: x, ">"),
        (lambda x: -x, lambda x: x, ">"),
        (lambda x: -x, lambda x: x, ">="),
        (lambda x: x, lambda x: [], "in"),
        (lambda x: x, lambda x: [x, 1, 2], "not in"),
        (lambda x: x, lambda x: not x, "is"),
        (lambda x: x, lambda x: x, "is not"),
    ],
)
def test_operator_map_callable_obj_assert_error(ucc_mock, left, right, operator):
    args = {"x": 1}
    with pytest.raises(AssertionError):
        ucc_mock.assert_util(left, right, operator, args, args)


@pytest.mark.parametrize(
    "left,right,operator",
    [
        (2, 2, "=="),
        ("a", "a", "=="),
        (True, True, "=="),
        (None, None, "=="),
        (1, 2, "!="),
        ("a", "b", "!="),
        (None, "a", "!="),
        (True, False, "!="),
        (1, 2, "<"),
        (False, True, "<"),
        ("a", "b", "<"),
        (1, 2, "<="),
        (2, 2, "<="),
        (False, True, "<="),
        (True, True, "<="),
        ("a", "b", "<="),
        ("a", "a", "<="),
        (2, 1, ">"),
        ("b", "a", ">"),
        (True, False, ">"),
        (2, 1, ">="),
        (1, 1, ">="),
        ("b", "a", ">="),
        (True, False, ">="),
        ("a", "a", ">="),
        (False, False, ">="),
        (1, [1, 2, 3], "in"),
        ("1", "123", "in"),
        (1, [2, 3], "not in"),
        ("1", "", "not in"),
        (1, 1, "is"),
        ("a", "a", "is"),
        (True, True, "is"),
        (None, None, "is"),
        (None, object, "is not"),
        (1, "a", "is not"),
        (1, 2, "is not"),
        ("a", "b", "is not"),
    ],
)
def test_operator_map_pass(ucc_mock, left, right, operator):
    ucc_mock.assert_util(left, right, operator)


@pytest.mark.parametrize(
    "left,right,operator",
    [
        (1, 2, "=="),
        ("a", "b", "=="),
        (True, False, "=="),
        (None, 1, "=="),
        (1, 1, "!="),
        ("a", "a", "!="),
        (None, None, "!="),
        (True, True, "!="),
        (1, 1, "<"),
        (False, False, "<"),
        ("a", "a", "<"),
        (2, 1, "<="),
        (True, False, "<="),
        ("b", "a", "<="),
        (1, 2, ">"),
        ("a", "b", ">"),
        (False, True, ">"),
        (1, 2, ">="),
        ("a", "b", ">="),
        (False, True, ">="),
        (1, [2, 3], "in"),
        ("1", "23", "in"),
        (1, [1, 2, 3], "not in"),
        ("1", "12", "not in"),
        (1, 2, "is"),
        ("a", "b", "is"),
        (True, False, "is"),
        (object, None, "is"),
        (None, None, "is not"),
        (1, 1, "is not"),
        ("a", "a", "is not"),
    ],
)
def test_operator_map_assert_error(ucc_mock, left, right, operator):
    with pytest.raises(AssertionError):
        ucc_mock.assert_util(left, right, operator)


@pytest.mark.parametrize(
    "exception", [TimeoutException, ElementNotInteractableException]
)
def test_exeption_in_assert_util(ucc_mock, exception):
    with patch("builtins.callable", side_effect=exception("important msg")):
        with pytest.raises(Exception, match="important msg"):
            ucc_mock.assert_util("left", "right")


def test_setup_class_ucc_tester():
    ucc_tester = UccTester()
    ucc_tester.setup_class()
    assert isinstance(ucc_tester.wait, selenium.webdriver.support.wait.WebDriverWait)
    assert ucc_tester.wait._timeout == 20


SESSION_KEY = "1234"


@pytest.fixture()
def mock_request():
    mock = MagicMock()
    mock.json = lambda: {"sessionKey": SESSION_KEY}
    return mock


defaults_rest_helper = {
    "splunk_mgmt_url": "https://localhost:8089",
    "username": "admin",
    "password": "Chang3d!",
}


def test_rest_helper(mock_request):
    with patch("requests.post", return_value=mock_request):
        rest_helper = RestHelper(**defaults_rest_helper)
    assert rest_helper.session_key == SESSION_KEY
    assert rest_helper.splunk_mgmt_url == defaults_rest_helper.get("splunk_mgmt_url")
    assert rest_helper.username == defaults_rest_helper.get("username")
    assert rest_helper.password == defaults_rest_helper.get("password")


@pytest.mark.parametrize(
    "side_effect",
    [
        Exception,
        lambda: {"messages": [{"type": "WARN"}]},
    ],
    ids=["test_exception_in_try_catch", "test_exception_login_failed"],
)
def test_rest_helper_exceptions(mock_request, side_effect):
    mock_request.json = side_effect
    with patch("requests.post", return_value=mock_request):
        with pytest.raises(Exception):
            RestHelper(**defaults_rest_helper)


expected_edge_opts = {
    "platform": "MAC",
    "browserName": "MicrosoftEdge",
    "ms:edgeOptions": {
        "extensions": [],
        "args": ["--ignore-ssl-errors=yes", "--ignore-certificate-errors"],
    },
    "ms:edgeChromium": True,
}


@pytest.mark.parametrize(
    "headless_run", [True, False], ids=["headless_run-True", "headless_run-False"]
)
@pytest.mark.parametrize(
    "platform,system",
    [("darwin", "MAC"), ("win", "WINDOWS"), ("cygwin", "WINDOWS"), ("unknow", "LINUX")],
)
def test_get_local_edge_opts(headless_run, platform, system):
    with patch("pytest_splunk_addon_ui_smartx.base_test.Edge"), patch(
        "sys.platform", platform
    ):
        selenium_helper = SeleniumHelper(
            **{**default_args_for_selenium_helper, "browser": "edge"}
        )
        assert selenium_helper.get_local_edge_opts(headless_run)["platform"] == system

        expected = deepcopy(expected_edge_opts)
        expected = {**expected, "platform": system}
        if headless_run:
            expected["ms:edgeOptions"]["args"].append("--headless")
            expected["ms:edgeOptions"]["args"].append("--window-size=1280,768")

        assert selenium_helper.get_local_edge_opts(headless_run) == expected


@pytest.mark.parametrize(
    "headless_run", [True, False], ids=["headless_run-True", "headless_run-False"]
)
def test_get_local_chrome_opts(headless_run):
    with patch("selenium.webdriver.Chrome"):
        selenium_helper = SeleniumHelper(**default_args_for_selenium_helper)
        local_chrome_opts = selenium_helper.get_local_chrome_opts(headless_run)
        assert isinstance(local_chrome_opts, selenium.webdriver.chrome.options.Options)
        assert "--ignore-ssl-errors=yes" in local_chrome_opts.arguments
        assert "--ignore-certificate-errors" in local_chrome_opts.arguments
        if headless_run:
            assert "--headless" in local_chrome_opts.arguments
            assert "--window-size=1280,768" in local_chrome_opts.arguments


def test_login_to_splunk():
    with patch("selenium.webdriver.Chrome"), patch(
        "pytest_splunk_addon_ui_smartx.base_test.LoginPage",
        side_effect=Exception("important msg"),
    ):
        with pytest.raises(Exception, match="important msg"):
            selenium_helper = SeleniumHelper(**default_args_for_selenium_helper)
            selenium_helper.login_to_splunk()


@pytest.mark.parametrize("status", [True, False])
def test_update_sauce_job(status):
    import pytest_splunk_addon_ui_smartx.base_test

    importlib.reload(pytest_splunk_addon_ui_smartx.base_test)
    with patch("selenium.webdriver.Remote"), patch("requests.put") as req, patch(
        "os.environ.get", lambda x: x
    ):
        selenium_helper = pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper(
            **{**default_args_for_selenium_helper, "debug": False}
        )
        selenium_helper.browser_session = "1234"
        selenium_helper.update_saucelab_job(status)
        req.assert_called_with(
            "https://saucelabs.com/rest/v1/SAUCE_USERNAME/jobs/1234",
            auth=("SAUCE_USERNAME", "SAUCE_PASSWORD"),
            data='{"passed": false}' if status else '{"passed": true}',
        )
