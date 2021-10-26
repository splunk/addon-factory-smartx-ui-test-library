#
# Copyright 2021 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from selenium.webdriver.common.by import By

from ..base_component import BaseComponent, Selector


class BaseControl(BaseComponent):
    """
    Purpose:
    The base class for the controls present in the entity. It is implemented to simplify accessing of controls.
    """

    def __init__(self, browser, container):
        """
        :param browser: The instance of the selenium webdriver
        :param container: The container in which the component is located at.
        """
        super().__init__(browser, container)
        self.elements.update(
            {"help_text": Selector(select=container.select + ' [data-test="help"]')}
        )
        self.elements.update(
            {
                "label_text": Selector(
                    select=container.select + ' [data-test="label"][id]'
                )
            }
        )
        self.elements.update(
            {
                "tooltip_icon": Selector(
                    select=container.select + ' [data-test="tooltip"]'
                )
            }
        )
        self.elements.update(
            {"tooltip_text": Selector(select='[data-test="screen-reader-content"]')}
        )
        self.browser = browser

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
        GET_PARENT_ELEMENT = (
            "if(arguments[0].hasChildNodes()){var r='';var C=arguments[0].childNodes;"
            "for(var n=0;n<C.length;n++){if(C[n].nodeType==Node.TEXT_NODE){r+=' '+C[n].nodeValue}}"
            "return r.trim()}else{return arguments[0].innerText}"
        )
        parent_text = self.browser.execute_script(GET_PARENT_ELEMENT, self.label_text)
        return parent_text
