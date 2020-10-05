
from ..components.tabs import Tab
from ..components.entity import Entity
from ..components.controls.single_select import SingleSelect
from ..components.entity import Entity
from ..components.controls.checkbox import Checkbox
from ..components.controls.button import Button
from ..components.controls.textbox import TextBox
from ..backend_confs import SingleBackendConf
from selenium.webdriver.common.by import By
import time


class Proxy(Entity):

    def __init__(self, ucc_smartx_configs, ta_name, ta_conf = ""):
        """
            :param browser: The selenium webdriver
            :param urls: Splunk web & management url. {"web": , "mgmt": }
            :param session_key: session key to access the rest endpoints
        """
        entity_container = {"by": By.CSS_SELECTOR, "select": "#proxy-tab"}
        super(Proxy, self).__init__(ucc_smartx_configs.browser, entity_container)
        self.splunk_web_url = ucc_smartx_configs.splunk_web_url
        self.splunk_mgmt_url = ucc_smartx_configs.splunk_mgmt_url
        self.ta_name = ta_name
        self.ta_conf = ta_conf
        if self.ta_conf == "":
            self.ta_conf = "conf-{}_settings".format(self.ta_name.lower())

        self.open()


        # Controls
        self.host = TextBox(ucc_smartx_configs.browser, {"by": By.NAME, "select": "proxy_url"})
        self.port = TextBox(ucc_smartx_configs.browser, {"by": By.NAME, "select": "proxy_port"})
        self.username = TextBox(ucc_smartx_configs.browser, {"by": By.NAME, "select": "proxy_username"})
        self.password = TextBox(ucc_smartx_configs.browser, {"by": By.NAME, "select": "proxy_password"}, encrypted=True)
        self.proxy_enable = Checkbox(ucc_smartx_configs.browser, {"by": By.CSS_SELECTOR, "select": " .proxy_enabled" })
        self.dns_enable = Checkbox(ucc_smartx_configs.browser, {"by": By.CSS_SELECTOR, "select": " .proxy_rdns" })
        
        # Components
        self.type = SingleSelect(
            ucc_smartx_configs.browser, {"by": By.CSS_SELECTOR, "select": ".proxy_type"})
       
        self.backend_conf = SingleBackendConf(self._get_proxy_endpoint(), ucc_smartx_configs.session_key)

    def open(self):
        """
        Open the required page. Page(super) class opens the page by default.
        """
        self.browser.get(
            '{}/en-US/app/{}/configuration'.format(self.splunk_web_url, self.ta_name))
        tab = Tab(self.browser)
        tab.open_tab("proxy")


    def _get_proxy_endpoint(self):
        """
        get rest endpoint for the configuration
        """
        return '{}/servicesNS/nobody/{}/configs/{}/proxy'.format(self.splunk_mgmt_url, self.ta_name, self.ta_conf)
