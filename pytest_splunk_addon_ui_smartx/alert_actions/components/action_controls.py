# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from .alert_base_component import Selector
from .alert_base_control import AlertBaseControl
from selenium.webdriver.common.by import By
from lxml.cssselect import CSSSelector


class ActionControls(AlertBaseControl):

    def __init__(self, browser, container):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
            :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        super(ActionControls, self).__init__(browser, container)
        select_xpath = CSSSelector(container.select).path
        self.elements.update({
            "help_text": Selector(by=By.XPATH, select= select_xpath + "//following::span[contains(@class, 'help-block')][1]"),
            "label_text": Selector(by=By.XPATH, select= select_xpath + "//preceding::label[contains(@class, 'control-label')][1]")
        })