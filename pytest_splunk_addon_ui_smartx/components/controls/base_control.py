# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ..base_component import BaseComponent, Selector
from selenium.webdriver.common.by import By

class BaseControl(BaseComponent):
    """
    Purpose:
    The base class for the controls present in the entity. It iss implemented to simplify accessing of controls.
    """
    
    def __init__(self, browser, container):
        """
            :param browser: The instance of the selenium webdriver 
            :param container: The container in which the component is located at.
        """   
        super(BaseControl, self).__init__(browser, container)
        self.elements.update({
            "help_text": Selector(select=container.select + " span.help-block")
        })

    def get_help_text(self):
        return self.get_clear_text(self.help_text)