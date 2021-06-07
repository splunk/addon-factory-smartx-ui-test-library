# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from .alert_base_component import AlertBaseComponent, Selector
from selenium.webdriver.common.by import By

class AlertBaseControl(AlertBaseComponent):
    """
    Purpose:
    The base class for the controls present in the entity. It is implemented to simplify accessing of controls.
    """
    
    def __init__(self, browser, container):
        """
            :param browser: The instance of the selenium webdriver 
            :param container: The container in which the component is located at.
        """   
        super(AlertBaseControl, self).__init__(browser, container)
        self.elements.update({
            "help_text": Selector(select=container.select + " span.help-block")
        })
        self.elements.update({
            "label_text": Selector(select=container.select + " .control-label")
        })
        self.elements.update({
            "tooltip_icon": Selector(select=container.select + " .tooltip-link")
        })
        self.elements.update({
            "tooltip_text": Selector(select=".tooltip-inner")
        })
    
    def get_tooltip_text(self):
        self.hover_over_element("tooltip_icon")
        self.wait_for("tooltip_text")
        return self.get_clear_text(self.tooltip_text)

    def get_help_text(self):
        return self.get_clear_text(self.help_text)

    def get_input_label(self):
        """
        get field label value
        """
        return self.get_clear_text(self.label_text)