from __future__ import absolute_import
from .page import Page
from ..components.login import Login
from selenium.webdriver.common.by import By

class LoginPage(Page):
    """
    Page: Login page
    """
    def __init__(self, ucc_smartx_configs):

        super(LoginPage, self).__init__(ucc_smartx_configs)
        self.login = Login(ucc_smartx_configs.browser)
