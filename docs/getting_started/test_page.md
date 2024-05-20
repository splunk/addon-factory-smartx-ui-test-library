When creating new UI tests for a Splunk App using SmartX, it would be helpful to start with creating the TA's page class files within test/ui/&lt;TA&gt;_UccLib.

These files should contain Page classes that represent the webpage we want to test within the app, and hold the multiple components that are within that webpage. The class should also contain the webdriver instance and the backend methods to make API calls to Splunk.

When creating a Page file, there are usually 2 portions of it to create:

**1. The page class**
This would be the main class for the page file, which should hold all of the components and class instances for calling the backend.
This file would also need to import all of the components as well from SmartX to be able to use them.
The usual parameters for this class are the following:

 - ucc_smartx_selenium_helper (SmartX fixture): The SmartX instance for the selenium webdriver which helps control page interactions for the tests. This parameter is used to create the UI components, and we should not create the UI component classes without this parameter.
 - ucc_smartx_rest_helper (SmartX fixture): The SmartX instance for the selenium helper which helps control page interactions. This parameter holds the selenium driver, urls(web, mgmt) and session key for the tests. This parameter is used for creating SmartX rest classes such as the classes found within backend_confs.py.
 - open_page(Flag): This parameter is to indicate whether or not we should open this webpage when we create this class instance. If we want to open the file later, we can use &lt;class&gt;.open() later on.

This class should also hold functions to open the webpage and to store the backend endpoint.

**2. The entities found within the page**
If the webpage consists of any entities (A web element on a page that consists of multiple components, such as popups or forms to create a new input). then you would need to create an entity that represents the entity's controls and components.
The usual parameters for this class are the following:

 - browser: The selenium webdriver
 - container: The container in which the entity is located in

The parent class for this type of class is found within the `pytest_splunk_addon_ui_smartx/components/entity.py` file. This base class has useful functions to click on a save button in the entity, closing the entity, and getting messages that may appear.
This base class has the following parameters:

 - browser: The selenium webdriver
 - container: Container in which the entity is located.
 - add_btn: The locator of add_button with which the entity will be opened

**Example**
A Example Page file would look like this:

```python
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

```
