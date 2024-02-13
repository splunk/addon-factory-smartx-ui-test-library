#
# Copyright 2024 Splunk Inc.
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

from selenium.webdriver.common.by import By

from .base_component import BaseComponent, Selector


class MessageTray(BaseComponent):
    """
    Component: MessageTray
    Base class of Input & Configuration table
    """

    def __init__(self, browser, mapping=dict()):
        """
        :param browser: The selenium webdriver
        :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
        :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        container = Selector(
            select="[data-view='views/shared/splunkbar/messages/MenuContents']"
        )
        super().__init__(browser, container)
        self.elements.update(
            {
                "message_tray_dropdown": Selector(select="[title='Messages']"),
                "message_row": Selector(
                    select=container.select + " [data-view$='Message']"
                ),
                "delete_btn": Selector(
                    select=container.select + " [data-action='delete']"
                ),
                "msg_text": Selector(
                    select=container.select + " [data-role='content']"
                ),
                "no_msgs": Selector(
                    select=container.select + " [data-role='no-messages']"
                ),
                "delete_all_btn": Selector(
                    select=container.select + " [title='Delete All']"
                ),
                "msg_icon": Selector(
                    select=container.select + "  [data-role='icon'] [data-view$='Icon']"
                ),
            }
        )

    def open(self):
        self.wait_for("message_tray_dropdown")
        self.wait_to_be_clickable("message_tray_dropdown")
        self.message_tray_dropdown.click()

    def wait_for_msg(self):
        """
        Wait for error message in message tray
        """
        current_msg_count = self.get_msg_count()

        def _wait_for_msg(driver):
            return (
                self.get_msg_count() > 0 and self.get_icon_attribute(0) == "error"
            ) or self.get_msg_count() > current_msg_count

        self.wait_for(_wait_for_msg, timeout=120)

    def get_message_list(self):
        """
        Returns a generator list for the messages in the message tray
            :return: Returns Generator list of values
        """
        return [each.text.strip() for each in self.get_elements("msg_text")]

    def get_msg_count(self):
        """
        Count the number of msgs in the message tray.
            :return: Int The count of the msgs
        """
        return len(list(self._get_rows()))

    def delete_msg(self, value):
        """
        Deletes the message that appears after the first few rows for the messageTray
        """
        _row = self._get_row(value)
        _row.find_element(*list(self.elements["delete_btn"]._asdict().values())).click()
        return True

    def delete_all_msgs(self):
        """
        Clock on Delete All for the MessageTray
            :return: Bool if successful
        """
        self.delete_all_btn.click()
        return self.no_msgs.text.strip()

    def get_msg(self, value):
        """
        Returns the message at row number
            :return: Str message
        """
        _row = self._get_row(value)
        return _row.find_element(
            *list(self.elements["msg_text"]._asdict().values())
        ).text.strip()

    def get_icon_attribute(self, value):
        """
        Returns the type of icon within the msg
            :value: The msg at row value
            :return: The icon attribute value in the msg
        """
        _row = self._get_row(value)
        return (
            _row.find_element(*list(self.elements["msg_icon"]._asdict().values()))
            .get_attribute("data-icon")
            .strip()
        )

    def _get_rows(self):
        """
        Get list of msgs
            :return: The list of msgs within the component
        """
        yield from self.get_elements("message_row")

    def _get_row(self, value):
        """
        Get the specified message at row.
        :param name: row name
            :return: element Gets the row specified within the messageTray, or raises a warning if not found
        """
        rows = list(self._get_rows())
        try:
            return rows[value]
        except:
            raise ValueError("Row number {} not found in messageTray".format(value))
