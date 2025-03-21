from pytest_splunk_addon_ui_smartx.components.controls.checkboxgroup import (
    CheckboxGroup,
)
from pytest_splunk_addon_ui_smartx.pages.page import Page
from pytest_splunk_addon_ui_smartx.components.base_component import Selector
from pytest_splunk_addon_ui_smartx.components.base_component import BaseComponent
from pytest_splunk_addon_ui_smartx.components.dropdown import Dropdown
from pytest_splunk_addon_ui_smartx.components.entity import Entity
from pytest_splunk_addon_ui_smartx.components.controls.button import Button
from pytest_splunk_addon_ui_smartx.components.controls.checkbox import Checkbox
from pytest_splunk_addon_ui_smartx.components.controls.learn_more import LearnMore
from pytest_splunk_addon_ui_smartx.components.controls.textbox import TextBox
from pytest_splunk_addon_ui_smartx.components.controls.textarea import TextArea
from pytest_splunk_addon_ui_smartx.components.controls.single_select import SingleSelect
from pytest_splunk_addon_ui_smartx.components.controls.multi_select import MultiSelect
from pytest_splunk_addon_ui_smartx.components.controls.message import Message
from pytest_splunk_addon_ui_smartx.components.input_table import InputTable
from pytest_splunk_addon_ui_smartx.backend_confs import ListBackendConf
from pytest_splunk_addon_ui_smartx.components.controls.toggle import Toggle

from selenium.webdriver.common.by import By


class ExampleInputOne(Entity):
    """
    Form to configure a new Input
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The container in which the entity is located in
        """
        add_btn = Button(
            browser, Selector(select=container.select + '[id="addInputBtn"]')
        )
        entity_container = Selector(select='[data-test="modal"]')

        super().__init__(browser, entity_container, add_btn=add_btn)

        # Controls
        self.name = TextBox(
            browser, Selector(select=' [data-test="control-group"][data-name="name"]')
        )
        self.example_checkbox = Checkbox(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="input_one_checkbox"]'
            ),
        )
        self.example_radio = Toggle(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="input_one_radio"]'
            ),
        )
        self.single_select_group_test = SingleSelect(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="singleSelectTest"]'
            ),
            allow_new_values=True,
        )
        self.multiple_select_test = MultiSelect(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="multipleSelectTest"]'
            ),
        )
        self.interval = TextBox(
            browser,
            Selector(select=' [data-test="control-group"][data-name="interval"]'),
        )
        self.index = SingleSelect(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="index"]'
            ),
            allow_new_values=True,
        )
        self.example_account = SingleSelect(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="account"]'
            ),
        )
        self.object = TextBox(
            browser, Selector(select=' [data-test="control-group"][data-name="object"]')
        )
        self.object_fields = TextBox(
            browser,
            Selector(select=' [data-test="control-group"][data-name="object_fields"]'),
        )
        self.order_by = TextBox(
            browser,
            Selector(select=' [data-test="control-group"][data-name="order_by"]'),
        )
        self.query_start_date = TextBox(
            browser,
            Selector(select=' [data-test="control-group"][data-name="start_date"]'),
        )
        self.limit = TextBox(
            browser, Selector(select=' [data-test="control-group"][data-name="limit"]')
        )
        self.help_link = LearnMore(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="example_help_link"]'
            ),
        )
        self.text_area = TextArea(
            browser,
            Selector(
                select=entity_container.select + ' [data-name="example_textarea_field"]'
            ),
        )
        self.title = BaseComponent(browser, Selector(select=' [data-test="title"]'))


class ExampleInputTwo(Entity):
    """
    Form to configure a new Input
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The container in which the entity is located in
        """
        add_btn = Button(
            browser, Selector(select=container.select + ' [id="addInputBtn"]')
        )
        entity_container = Selector(select=' [data-test="modal"]')

        super().__init__(browser, entity_container, add_btn=add_btn)

        # Controls
        self.name = TextBox(
            browser, Selector(select='[data-test="control-group"][data-name="name"]')
        )
        self.interval = TextBox(
            browser,
            Selector(select=' [data-test="control-group"][data-name="interval"]'),
        )
        self.index = SingleSelect(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="index"]'
            ),
            allow_new_values=True,
        )
        self.example_account = SingleSelect(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="account"]'
            ),
        )
        self.example_multiple_select = MultiSelect(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="input_two_multiple_select"]'
            ),
        )
        self.example_checkbox = Checkbox(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="input_two_checkbox"]'
            ),
        )
        self.example_radio = Toggle(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="input_two_radio"]'
            ),
        )
        self.query_start_date = TextBox(
            browser,
            Selector(select=' [data-test="control-group"][data-name="start_date"]'),
        )
        self.help_link = LearnMore(
            browser,
            Selector(
                select=entity_container.select
                + ' [data-test="control-group"][data-name="example_help_link"]'
            ),
        )
        self.checkboxgroup = CheckboxGroup(
            browser, Selector(by=By.XPATH, select="//div[@type='checkboxGroup']")
        )
        self.title = BaseComponent(browser, Selector(select=' [data-test="title"]'))


class ExampleInputThree(Entity):
    """
    Form to configure a new Input
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The container in which the entity is located in
        """
        add_btn = Button(
            browser, Selector(select=container.select + ' [id="addInputBtn"]')
        )
        entity_container = Selector(select=' [data-test="modal"]')

        super().__init__(browser, entity_container, add_btn=add_btn)

        # Controls
        self.name = TextBox(
            browser, Selector(select='[data-test="control-group"][data-name="name"]')
        )
        self.interval = TextBox(
            browser,
            Selector(select=' [data-test="control-group"][data-name="interval"]'),
        )


class ExampleInputFour(Entity):
    """
    Form to configure a new Input
    """

    def __init__(self, browser, container):
        """
        :param browser: The selenium webdriver
        :param container: The container in which the entity is located in
        """
        add_btn = Button(
            browser, Selector(select=container.select + ' [id="addInputBtn"]')
        )
        entity_container = Selector(select=' [data-test="modal"]')

        super().__init__(browser, entity_container, add_btn=add_btn)

        # Controls
        self.name = TextBox(
            browser, Selector(select='[data-test="control-group"][data-name="name"]')
        )
        self.interval = TextBox(
            browser,
            Selector(select=' [data-test="control-group"][data-name="interval"]'),
        )


class InputPage(Page):
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
        :param browser: The selenium webdriver
        :param urls: Splunk web & management url. {"web": , "mgmt": }
        :param session_key: session key to access the rest endpoints
        """
        super().__init__(ucc_smartx_selenium_helper, ucc_smartx_rest_helper, open_page)

        input_container = Selector(select=' div[role="main"]')
        if ucc_smartx_selenium_helper:
            self.title = Message(
                ucc_smartx_selenium_helper.browser,
                Selector(select=' [data-test="column"] .pageTitle'),
            )
            self.description = Message(
                ucc_smartx_selenium_helper.browser,
                Selector(select=' [data-test="column"] .pageSubtitle'),
            )
            self.create_new_input = Dropdown(
                ucc_smartx_selenium_helper.browser,
                Selector(select='[id="addInputBtn"]'),
            )
            self.table = InputTable(
                ucc_smartx_selenium_helper.browser,
                input_container,
                mapping={"status": "disabled", "input_type": 3},
            )
            self.entity1 = ExampleInputOne(
                ucc_smartx_selenium_helper.browser, input_container
            )
            self.entity2 = ExampleInputTwo(
                ucc_smartx_selenium_helper.browser, input_container
            )
            self.entity3 = ExampleInputThree(
                ucc_smartx_selenium_helper.browser, input_container
            )
            self.entity4 = ExampleInputFour(
                ucc_smartx_selenium_helper.browser, input_container
            )
            self.pagination = Dropdown(
                ucc_smartx_selenium_helper.browser, Selector(select=".dropdownPage")
            )
            self.type_filter = Dropdown(
                ucc_smartx_selenium_helper.browser, Selector(select=".dropdownInput")
            )

        if ucc_smartx_rest_helper:
            self.backend_conf = ListBackendConf(
                self._get_input_endpoint(),
                ucc_smartx_rest_helper.username,
                ucc_smartx_rest_helper.password,
            )

    def open(self):
        self.browser.get(
            "{}/en-US/app/Splunk_TA_UCCExample/inputs".format(self.splunk_web_url)
        )

    def _get_input_endpoint(self):
        return "{}/servicesNS/nobody/Splunk_TA_UCCExample/configs/conf-inputs".format(
            self.splunk_mgmt_url
        )
