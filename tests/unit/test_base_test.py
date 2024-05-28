from copy import deepcopy
from unittest.mock import MagicMock, patch

import pytest
import selenium
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException

import pytest_splunk_addon_ui_smartx.base_test
from pytest_splunk_addon_ui_smartx.base_test import (
    RestHelper,
    SeleniumHelper,
    UccTester,
)

default_args_for_selenium_helper = {
    "browser": "chrome",
    "browser_version": "88",
    "splunk_web_url": "https://localhost:8000",
    "splunk_mgmt_url": "https://localhost:8089",
    "local_run": True,
    "cred": ("admin", "Chang3d!"),
    "headless": False,
    "test_case": None,
}


def test_selenium_helper_raise_exception_with_given_invalid_browser_version():
    with pytest.raises(Exception, match="No valid browser found.") as e, patch(
        "os.environ.get", lambda x: x if x != "SELENIUM_HOST" else None
    ):
        SeleniumHelper(**{**default_args_for_selenium_helper, "browser": "aa"})


@pytest.mark.parametrize(
    "browser,webdriver, local_run",
    [
        ("firefox", "selenium.webdriver.Firefox", [True, False]),
        ("chrome", "selenium.webdriver.Chrome", [True, False]),
        ("IE", "selenium.webdriver.Ie", True),
        ("safari", "selenium.webdriver.Safari", True),
        ("edge", "pytest_splunk_addon_ui_smartx.base_test.Edge", True),
    ],
)
def test_constructor_selenium_helper(browser, webdriver, local_run):
    with patch(webdriver if local_run else "selenium.webdriver.Remote"), patch(
        "os.environ.get", lambda x: x
    ):
        pytest_splunk_addon_ui_smartx.base_test.SeleniumHelper(
            **{
                **default_args_for_selenium_helper,
                "browser": browser,
                "local_run": local_run,
                "browser_version": 11,
            }
        )


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
            firefox_options="firefox_opts"
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
            service_args=["--verbose"],
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
        assert SeleniumHelper.get_local_edge_opts(headless_run)["platform"] == system
        expected = deepcopy(expected_edge_opts)
        expected = {**expected, "platform": system}
        if headless_run:
            expected["ms:edgeOptions"]["args"].append("--headless")
            expected["ms:edgeOptions"]["args"].append("--window-size=1280,768")

        assert SeleniumHelper.get_local_edge_opts(headless_run) == expected


# @pytest.mark.parametrize(
#     "headless_run", [True, False], ids=["headless_run-True", "headless_run-False"]
# )
# def test_get_local_chrome_opts(headless_run):
#     with patch("selenium.webdriver.Chrome"):
#         local_chrome_opts = SeleniumHelper.get_local_chrome_opts(headless_run)
#         assert isinstance(local_chrome_opts, selenium.webdriver.chrome.options.Options)
#         assert "--ignore-ssl-errors=yes" in local_chrome_opts.arguments
#         assert "--ignore-certificate-errors" in local_chrome_opts.arguments
#         if headless_run:
#             assert "--headless" in local_chrome_opts.arguments
#             assert "--window-size=1280,768" in local_chrome_opts.arguments


def test_login_to_splunk():
    with patch("selenium.webdriver.Chrome"), patch(
        "pytest_splunk_addon_ui_smartx.base_test.LoginPage",
        side_effect=Exception("important msg"),
    ):
        with pytest.raises(Exception, match="important msg"):
            selenium_helper = SeleniumHelper(**default_args_for_selenium_helper)
            selenium_helper.login_to_splunk()
