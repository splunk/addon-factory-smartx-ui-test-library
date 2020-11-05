# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from .base_component import Selector, BaseComponent
from selenium.webdriver.common.by import By
import copy


class MessageTray(BaseComponent):
    """
     Component: Message Tray
    """
    def __init__(self, browser, container, mapping=dict(),wait_for_seconds = 10):
        """
            :param browser: The selenium webdriver
            :param container: Container in which the table is located. Of type dictionary: {"by":..., "select":...}
            :param mapping= If the table headers are different from it's html-label, provide the mapping as dictionary. For ex, {"Status": "disabled"}
        """
        
        super(MessageTray, self).__init__(browser, container)
        self.header_mapping = mapping
        
        self.elements.update({
            "msg_tray": Selector(select="[title^='Messages']"),
            "msgs_list": Selector(select="[data-role^='messages-list']"),
            "delete_btn": Selector(select="[data-action^='delete']"),
            "delete_all_btn": Selector(select="[title^='Delete All']"),
            "message_row": Selector(select="[data-view^='views/shared/splunkbar/messages/Message']"),
            "msg-text": Selector(select="[data-role^='content']"),
            "msg-icon": Selector(select="[data-view^='views/shared/splunkbar/messages/Message'] [data-role^='icon']"),
            "no_msgs": Selector(select="[data-role^='no-messages']")
        })
        self.wait_for_seconds = wait_for_seconds

    def get_msg_count(self):
        """
        Count the number of msgs in the component.
            :return: Int The count of the msgs
        """
        return len(list(self._get_rows()))

    def _get_rows(self):
        """
        Get list of msgs
            :return: The list of msgs within the component
        """
        for each_row in self.get_elements("message_row"):
            yield each_row
    
    def _get_row(self, value):
        """
        Get the specified row.
        :param name: row name 
            :return: element Gets the row specified within the messageTray, or raises a warning if not found
        """
        rows = list(self._get_rows())
        try:
            return rows[value]
        except:
            raise ValueError("Row number {} not found in messageTray".format(value)) 
    
    def _get_delete_btns(self):
        for each_btn in self.get_elements("delete_btn"):
            yield each_btn

    def delete_all_msgs(self):
        """
        Clock on Delete All for the MessageTray
            :return: Bool if successful
        """
        self.delete_all_btn.click()
        return self.no_msgs.text.strip()

    def delete_msg(self, value):
        """
        Deletes the message that appears after the first few rows for the messageTray
        """
        _row = self._get_row(value)
        _row.find_element(*list(self.elements["msg-text"]._asdict().values())).click()

    def get_msg(self, value):
        '''
        Returns the message at row number
            :return: Str message
        '''
        _row = self._get_row(value)
        return _row.find_element(*list(self.elements["delete_btn"]._asdict().values())).text.strip()

    def open(self):
        """
        Clicks on the msg_tray
            :return: Bool if successful
        """
        self.wait_to_be_clickable("msg_tray")
        self.msg_tray.click()
        return True

    def wait_for_rows_to_appear(self, row_count=1):
        """
        Wait for the messageTray to load the rows of messages
            :param row_count: number of row_count to wait for. 
        """
        def _wait_for_rows_to_appear(driver):
            return self.get_row_count() >= row_count
        self.wait_for(_wait_for_rows_to_appear, msg="Expected rows : {} to be greater or equal to {}".format(row_count, self.get_row_count()))
        
