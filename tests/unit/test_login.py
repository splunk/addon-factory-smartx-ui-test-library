from unittest.mock import MagicMock

from pytest_splunk_addon_ui_smartx.components.login import Login


def _browser_at(url, legacy_home_elements=0, login_form_elements=0):
    browser = MagicMock()
    browser.current_url = url

    def find_elements(_by, selector):
        if selector == '[data-test="header"], a[data-action="home"]':
            return [MagicMock()] * legacy_home_elements
        if selector == "form.loginForm":
            return [MagicMock()] * login_form_elements
        return []

    browser.find_elements.side_effect = find_elements
    return browser


def test_login_accepts_legacy_homepage_elements():
    browser = _browser_at(
        "https://splunk.example/en-US/app/search/search",
        legacy_home_elements=1,
    )

    assert Login.is_authenticated(browser) is True


def test_login_accepts_new_launcher_after_login_form_disappears():
    browser = _browser_at("https://splunk.example/en-GB/app/launcher/home")

    assert Login.is_authenticated(browser) is True


def test_login_rejects_launcher_path_while_login_form_remains():
    browser = _browser_at(
        "https://splunk.example/en-GB/app/launcher/home",
        login_form_elements=1,
    )

    assert Login.is_authenticated(browser) is False


def test_login_waits_for_any_supported_authenticated_shell():
    browser = MagicMock()
    login = Login(browser)
    username = MagicMock()
    password = MagicMock()
    login.get_element = MagicMock(
        side_effect=lambda key: {"username": username, "password": password}[key]
    )
    login.wait_for = MagicMock()

    login.login("admin", "password")

    condition = login.wait_for.call_args.args[0]
    assert condition(_browser_at("https://splunk.example/en-US/app/launcher/home"))
    assert (
        login.wait_for.call_args.args[1] == "Could not log in to the Splunk instance."
    )
