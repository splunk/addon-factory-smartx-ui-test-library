# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

# https://stackoverflow.com/questions/52947603/selenium-action-move-to-element-doesnt-work-in-safari-because-of-usupported/53633796#53633796


import selenium.webdriver

class ActionChains(selenium.webdriver.ActionChains):
    def __init__(self, driver):
        super(ActionChains, self).__init__(driver)
        if driver.name in ('Safari', 'Safari Technology Preview'):
            self.w3c_actions.key_action.pause = lambda *a, **k: None