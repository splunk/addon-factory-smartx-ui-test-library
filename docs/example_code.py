from selenium.webdriver.common.by import By

from pytest_splunk_addon_ui_smartx.backend_confs import ListBackendConf
from pytest_splunk_addon_ui_smartx.components.base_component import (
    BaseComponent,
    Selector,
)
from pytest_splunk_addon_ui_smartx.components.controls.button import Button
from pytest_splunk_addon_ui_smartx.components.controls.learn_more import LearnMore
from pytest_splunk_addon_ui_smartx.components.controls.message import Message
from pytest_splunk_addon_ui_smartx.components.controls.multi_select import MultiSelect
from pytest_splunk_addon_ui_smartx.components.controls.single_select import SingleSelect
from pytest_splunk_addon_ui_smartx.components.controls.textbox import TextBox
from pytest_splunk_addon_ui_smartx.components.controls.toggle import Toggle
from pytest_splunk_addon_ui_smartx.components.dropdown import Dropdown
from pytest_splunk_addon_ui_smartx.components.entity import Entity
from pytest_splunk_addon_ui_smartx.components.input_table import InputTable
from pytest_splunk_addon_ui_smartx.components.message_tray import MessageTray
from pytest_splunk_addon_ui_smartx.components.tabs import Tab
from pytest_splunk_addon_ui_smartx.pages.page import Page


class ExampleTAInputEntity(Entity):
    """
    Form to configure a new Input
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The container in which the entity is located in
        """
        add_btn = Button(browser, Selector(by=By.ID, select="addInputBtn"))
        entity_container = Selector(select='[data-test="modal"]')
        super().__init__(browser, entity_container, add_btn=add_btn)
        # Controls
        self.name = TextBox(
            browser, Selector(select='[data-test="control-group"][data-name="name"]')
        )
        self.interval = TextBox(
            browser,
            Selector(select='[data-test="control-group"][data-name="interval"]'),
        )
        self.index = SingleSelect(
            browser, Selector(select='[data-test="control-group"][data-name="index"]')
        )
        self.object = TextBox(
            browser, Selector(select='[data-test="control-group"][data-name="object"]')
        )
        self.object_fields = TextBox(
            browser,
            Selector(select='[data-test="control-group"][data-name="object_fields"]'),
        )
        self.title = BaseComponent(browser, Selector(select='[data-test="title"]'))
        self.use_existing_input = Toggle(
            browser,
            Selector(
                select='[data-test="control-group"][data-name="use_existing_checkpoint"]'
            ),
        )
        self.help_link = LearnMore(
            browser, Selector(select='[data-test="control-group"] [data-test="link"]')
        )


class ExampleTALogEntity(Entity):
    """
    Form to configure a new Input
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The container in which the entity is located in
        """
        add_btn = Button(browser, Selector(by=By.ID, select='[id="addInputBtn"]'))
        entity_container = Selector(select='[data-test="modal"]')
        super().__init__(browser, entity_container, add_btn=add_btn)
        # Controls
        self.name = TextBox(
            browser, Selector(select='[data-test="control-group"][data-name="name"]')
        )
        self.interval = TextBox(
            browser,
            Selector(select='[data-test="control-group"][data-name="interval"]'),
        )
        self.index = SingleSelect(
            browser, Selector(select='[data-test="control-group"][data-name="index"]')
        )
        self.title = BaseComponent(browser, Selector(select='[data-test="title"]'))
        self.use_existing_input = Toggle(
            browser,
            Selector(
                select='[data-test="control-group"][data-name="use_existing_checkpoint"]'
            ),
        )
        self.help_link = LearnMore(
            browser, Selector(select='[data-test="control-group"] [data-test="link"]')
        )


class Inputs(Page):
    """
    Page: Input page
    """

    def __init__(
        self,
        ucc_smartx_selenium_helper=None,
        ucc_smartx_rest_helper=None,
        open_page=True,
    ):
        """
        :param ucc_smartx_configs: smartx configuration fixture
        """
        super().__init__(
            ucc_smartx_selenium_helper, ucc_smartx_rest_helper, open_page=True
        )

        input_container = Selector(select='div[role="main"]')
        if ucc_smartx_selenium_helper:
            self.title = Message(
                ucc_smartx_selenium_helper.browser,
                Selector(select='[data-test="column"] .pageTitle'),
            )
            self.description = Message(
                ucc_smartx_selenium_helper.browser,
                Selector(select='[data-test="column"] .pageSubtitle'),
            )
            self.table = InputTable(
                ucc_smartx_selenium_helper.browser,
                input_container,
                mapping={"account_name": "account", "status": "disabled"},
            )
            self.create_new_input = Dropdown(
                ucc_smartx_selenium_helper.browser,
                Selector(by=By.ID, select="addInputBtn"),
            )
            self.ExampleTALogEntity = ExampleTALogEntity(
                ucc_smartx_selenium_helper.browser, input_container
            )
            self.ExampleTAInputEntity = ExampleTAInputEntity(
                ucc_smartx_selenium_helper.browser, input_container
            )
            self.pagination = Dropdown(
                ucc_smartx_selenium_helper.browser, Selector(select=".dropdownPage")
            )  # Selector for dropdown for selecting number of records shown in a single page
            self.type_filter = Dropdown(
                ucc_smartx_selenium_helper.browser, Selector(select=".dropdownInput")
            )  # Selector for dropdown for showing records of perticular input type.
            self.message_tray = MessageTray(ucc_smartx_selenium_helper.browser)

        if ucc_smartx_rest_helper:
            self.backend_conf = ListBackendConf(
                self._get_input_endpoint(),
                ucc_smartx_rest_helper.username,
                ucc_smartx_rest_helper.password,
            )

    def open(self):
        self.browser.get(
            "{}/en-US/app/Splunk_TA_<TA>/inputs".format(self.splunk_web_url)
        )

    def _get_input_endpoint(self):
        return "{}/servicesNS/nobody/Splunk_TA_<TA>/configs/conf-inputs".format(
            self.splunk_mgmt_url
        )


import pytest

from pytest_splunk_addon_ui_smartx.base_test import UccTester
from pytest_splunk_addon_ui_smartx.pages.proxy import Proxy

TA_NAME = "Splunk_TA_<TA_NAME>"
TA_PROXY_URL = (
    "/servicesNS/nobody/Splunk_TA_<TA_NAME>/Splunk_TA_<TA_NAME>_settings/proxy"
)

PROXY_TYPE_VALUES = ["http", "socks4", "socks5"]
DEFAULT_CONFIGURATION = {
    "proxy_enabled": "",
    "proxy_password": "",
    "proxy_port": "",
    "proxy_rdns": "",
    "proxy_type": "http",
    "proxy_url": "",
    "proxy_username": "",
}


@pytest.fixture(autouse=True)
def reset_configuration(ucc_smartx_rest_helper):
    yield
    proxy = Proxy(TA_NAME, TA_PROXY_URL, ucc_smartx_rest_helper=ucc_smartx_rest_helper)
    proxy.backend_conf_post.update_parameters(DEFAULT_CONFIGURATION)


class TestProxy(UccTester):
    """
    Test suite testing UCC from based configuration page
    """

    @pytest.mark.proxy
    @pytest.mark.forwarder
    def test_proxy_default_configs(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """
        Verifies the default proxy configurations
        """
        proxy = Proxy(
            TA_NAME,
            TA_PROXY_URL,
            ucc_smartx_selenium_helper=ucc_smartx_selenium_helper,
            ucc_smartx_rest_helper=ucc_smartx_rest_helper,
        )
        self.assert_util(proxy.proxy_enable.is_checked(), False)
        self.assert_util(proxy.dns_enable.is_checked(), False)
        self.assert_util(proxy.type.get_value(), "http")
        self.assert_util(proxy.host.get_value(), "")
        self.assert_util(proxy.port.get_value(), "")
        self.assert_util(proxy.username.get_value(), "")
        self.assert_util(proxy.password.get_value(), "")


ACCOUNT_PARAMS = {
    "name": "test_account",
    "endpoint": "login.test.com",
    "username": None,
    "password": None,
}


@pytest.fixture(scope="class", autouse=True)
def create_account(ucc_smartx_rest_helper):
    """
    Fixture to create account using rest endpoint
    """
    account = AccountPage(
        ucc_smartx_rest_helper=ucc_smartx_rest_helper, open_page=False
    )
    url = account._get_account_endpoint()
    account_config = {
        "name": ACCOUNT_PARAMS.get("name"),
        "endpoint": ACCOUNT_PARAMS.get("endpoint"),
        "username": ACCOUNT_PARAMS.get("username"),
        "password": ACCOUNT_PARAMS.get("password"),
    }
    account.backend_conf.post_stanza(url, account_config)
    yield
    account.backend_conf.delete_all_stanzas()


@pytest.fixture(scope="session", autouse=True)
def get_account_credentials():
    """
    Fixtures to fetch credentials from environment variables
    """
    ACCOUNT_PARAMS["username"] = b64decode(os.getenv("USERNAME")).decode("ascii")
    ACCOUNT_PARAMS["password"] = b64decode(os.getenv("PASSWORD")).decode("ascii")
    ACCOUNT_PARAMS["token"] = b64decode(os.getenv("TOKEN")).decode("ascii")
