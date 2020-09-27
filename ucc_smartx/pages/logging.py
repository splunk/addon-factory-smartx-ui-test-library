
from ..components.tabs import Tab
from ..components.entity import Entity
from ..components.controls.single_select import SingleSelect
from ..backend_confs import SingleBackendConf
from selenium.webdriver.common.by import By
import time


class Logging(Entity):
    def __init__(self, ucc_smartx_configs):
        """
            :param browser: The selenium webdriver
            :param urls: Splunk web & management url. {"web": , "mgmt": }
            :param session_key: session key to access the rest endpoints
        """
        entity_container = {"by": By.CSS_SELECTOR, "select": "#logging-tab"}
        super(Logging, self).__init__(ucc_smartx_configs.browser, entity_container)
        self.splunk_web_url = ucc_smartx_configs.splunk_web_url
        self.splunk_mgmt_url = ucc_smartx_configs.splunk_mgmt_url
        self.open()

        # Components
        self.log_level = SingleSelect(
            ucc_smartx_configs.browser, {"by": By.CSS_SELECTOR, "select": ".agent"})
        self.backend_conf = SingleBackendConf(
            self._get_logging_url(), ucc_smartx_configs.session_key)

    def open(self):
        """
        Open the required page. Page(super) class opens the page by default.
        """
        self.browser.get(
            '{}/en-US/app/Splunk_TA_microsoft-cloudservices/configuration'.format(self.splunk_web_url))
        tab = Tab(self.browser)
        tab.open_tab("logging")

    def _get_logging_url(self):
        """
        get rest endpoint for the configuration
        """
        return '{}/servicesNS/nobody/Splunk_TA_microsoft-cloudservices/configs/conf-splunk_ta_mscs_settings/logging'.format(self.splunk_mgmt_url)
