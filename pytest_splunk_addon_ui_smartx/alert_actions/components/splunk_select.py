#
# Copyright 2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from selenium.webdriver.support import select
from selenium.common.exceptions import UnexpectedTagNameException


class SplunkSelect(select.Select):
    def __init__(self, webelement):
        if not webelement.tag_name.lower() in ("select", "splunk-select"):
            raise UnexpectedTagNameException(
                "Select only works on <select> and <splunk-select> elements, "
                "not on <%s>" % webelement.tag_name
            )
        self._el = webelement
        multi = self._el.get_attribute("multiple")
        self.is_multiple = multi and multi != "false"
