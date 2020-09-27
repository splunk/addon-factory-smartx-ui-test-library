
from builtins import object
class Page(object):
    """
    Instance of a Page class holds all the components inside the page. To access the component, just do page.component.action_method()
    The page class should not have any interaction method for any visible components. It is supposed to hold all the components only.
    """

    def __init__(self, ucc_smartx_configs, open_page=True):
        """
            :param browser: The selenium webdriver
            :param urls: Splunk web & management url. {"web": , "mgmt": }
            :param session_key: session key to access the rest endpoints
        """

        self.browser = ucc_smartx_configs.browser
        self.splunk_web_url = ucc_smartx_configs.splunk_web_url
        self.splunk_mgmt_url = ucc_smartx_configs.splunk_mgmt_url
        if open_page:
            self.open()

    def open(self):
        """
        Abstract Method. Open the page
        """
        self.browser.get(self.splunk_web_url)
