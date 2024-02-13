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

import copy
import re
from contextlib import contextmanager

from selenium.common import exceptions

from .action_controls import ActionControls
from .alert_base_component import Selector
from .alert_base_control import AlertBaseControl


class AlertTable(ActionControls):
    def __init__(self, browser, mapping=dict(), wait_for_seconds=10):
        container = Selector(select=".grid-placeholder")
        super().__init__(browser, container)
        self.header_mapping = mapping
        self.elements.update(
            {
                "rows": Selector(
                    select=container.select + " tr.list-item.savedsearches-gridrow"
                ),
                "header": Selector(select=container.select + " th"),
                "col": Selector(select=container.select + " td.cell-{column}"),
                "app_listings": Selector(select=container.select + " tbody"),
                "action_values": Selector(
                    select=container.select + " td.col-actions a"
                ),
                "col-number": Selector(
                    select=container.select + " td:nth-child({col_number})"
                ),
                "edit": Selector(select="a.edit"),
                "clone": Selector(select="a.clone"),
                "delete": Selector(select="a.delete"),
                "delete_prompt": Selector(select=".modal-dialog div.delete-prompt"),
                "delete_btn": Selector(select=".modal-dialog .submit-btn"),
                "delete_cancel": Selector(select=".modal-dialog .cancel-btn"),
                "delete_close": Selector(select=".modal-dialog button.close"),
                "delete_loading": Selector(select=".modal-dialog .msg-loading"),
                "waitspinner": Selector(
                    select=container.select + " div.shared-waitspinner"
                ),
                "count": Selector(select=container.select + " .shared-collectioncount"),
                "filter": Selector(select=container.select + " input.search-query"),
                "filter_clear": Selector(select=container.select + " a.control-clear"),
                "more_info": Selector(select=container.select + " td.expands"),
                "more_info_row": Selector(
                    select=container.select + " tr.expanded + tr"
                ),
                "more_info_key": Selector(select="dt"),
                "more_info_value": Selector(select="dd"),
                "switch_to_page": Selector(
                    select=container.select + " .pull-right li a"
                ),
                "alert_sign": Selector(
                    select=container.select + " td.col-{column} .alert"
                ),
            }
        )
        self.wait_for_seconds = wait_for_seconds

    def get_count_title(self):
        """
        Get the count mentioned in the table title
            :return: Str The count of the table title
        """
        return self.get_clear_text(self.count)

    def get_row_count(self):
        """
        Count the number of rows in the page.
            :return: Int The count of the table rows
        """
        return len(list(self._get_rows()))

    def get_headers(self):
        """
        Get list of headers from the table
            :return: Generator for Str list The headers in the table
        """
        return [self.get_clear_text(each) for each in self.get_elements("header")]

    def get_sort_order(self):
        """
        Get the column-header which is sorted rn.
            Warning: It depends on the class of the headers and due to it, the returned result might give wrong answer.
            :returns: a dictionary with the "header" & "ascending" order
        """
        for each_header in self.get_elements("header"):
            if re.search(r"\basc\b", each_header.get_attribute("class")):
                return {"header": self.get_clear_text(each_header), "ascending": True}
            elif re.search(r"\bdesc\b", each_header.get_attribute("class")):
                return {"header": self.get_clear_text(each_header), "ascending": False}

    def sort_column(self, column, ascending=True):
        """
        Sort a column in ascending or descending order
            :param column: The header of the column which should be sorted
            :param ascending: True if the column should be sorted in ascending order, False otherwise
        """
        for each_header in self.get_elements("header"):

            if self.get_clear_text(each_header).lower() == column.lower():
                if "asc" in each_header.get_attribute("class") and ascending:
                    # If the column is already in ascending order, do nothing
                    return
                elif "asc" in each_header.get_attribute("class") and not ascending:
                    # If the column is in ascending order order and we want to have descending order, click on the column-header once
                    each_header.click()
                    self._wait_for_loadspinner()
                    return
                elif "desc" in each_header.get_attribute("class") and not ascending:
                    # If the column is already in descending order, do nothing
                    return
                elif "desc" in each_header.get_attribute("class") and ascending:
                    # If the column is in descending order order and we want to have ascending order, click on the column-header once
                    each_header.click()
                    self._wait_for_loadspinner()
                    return
                else:
                    # The column was not sorted before
                    if ascending:
                        # Click to sort ascending order
                        each_header.click()
                        self._wait_for_loadspinner()
                        return
                    else:
                        # Click 2 times to sort in descending order

                        # Ascending
                        each_header.click()
                        self._wait_for_loadspinner()
                        # Decending
                        # The existing element changes (class will be changed), hence, it can not be referenced again.
                        # So we need to get the headers again and do the same process.
                        self.sort_column(column, ascending=False)
                        return

    def _wait_for_loadspinner(self):
        """
        There exist a loadspinner when sorting/filter has been applied. This method will wait until the spinner is dissapeared
        """
        try:
            self.wait_for("waitspinner", timeout=5)
            self.wait_until("waitspinner")
        except:
            print("Waitspinner did not appear")

    def wait_for_rows_to_appear(self, row_count=1):
        """
        Wait for the table to load row_count rows
            :param row_count: number of row_count to wait for.
        """

        def _wait_for_rows_to_appear(driver):
            return self.get_row_count() >= row_count

        self.wait_for(
            _wait_for_rows_to_appear,
            msg="Expected rows : {} to be greater or equal to {}".format(
                row_count, self.get_row_count()
            ),
        )

    def wait_for_column_to_appear(self, column_name):
        """
        Wait for the table to load the column with the given column name.
            :param column_name: Name of the column to wait for.
        """

        def _wait_for_column_to_appear(driver):
            return column_name in self.get_headers()

        self.wait_for(
            _wait_for_column_to_appear,
            msg="Column {} not found in the table".format(column_name),
        )

    def get_table(self):
        """
        Get whole table in dictionary form. The row_name will will be the key and all header:values will be it's value. {row_1 : {header_1: value_1, . . .}, . . .}
            :return: dict The data within the table
        """

        table = dict()
        headers = list(self.get_headers())

        for each_row in self._get_rows():
            row_name = self._get_column_value(each_row, "name")
            table[row_name] = dict()
            for each_col in headers:
                each_col = each_col.lower()
                if each_col:
                    table[row_name][each_col] = self._get_column_value(
                        each_row, each_col
                    )
        return table

    def get_cell_value(self, name, column):
        """
        Get a specific cell value.
            :param name: row_name of the table
            :param column: column header of the table
            :return: str The value within the cell that we are looking for
        """
        _row = self._get_row(name)
        return self._get_column_value(_row, column)

    def get_column_values(self, column):
        """
        Get list of values of  column
            :param column: column header of the table
            :return: List The values within the certain column
        """
        value_list = []
        for each_row in self._get_rows():
            value_list.append(self._get_column_value(each_row, column))
        return value_list

    def get_list_of_actions(self, name):
        """
        Get list of possible actions for a specific row
            :param name: The name of the row
            :return: Generator List The list of actions available within a certain row of the table
        """
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["action_values"]._asdict().values()))
        return [
            self.get_clear_text(each_element)
            for each_element in self.get_elements("action_values")
        ]

    def edit_row(self, name):
        """
        Edit the specified row. It will open the edit form(entity). The opened entity should be interacted with instance of entity-class only.
            :param name: row_name of the table
        """
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["edit"]._asdict().values())).click()

    def clone_row(self, name):
        """
        Clone the specified row. It will open the edit form(entity). The opened entity should be interacted with instance of entity-class only.
            :param name: row_name of the table
        """
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["clone"]._asdict().values())).click()

    def delete_row(self, name, cancel=False, close=False, prompt_msg=False):
        """
        Delete the specified row. Clicking on delete will open a pop-up. Delete the row if neither of (cancel, close) specified.
            :param name: row_name of the table
            :param cancel: if provided, after the popup is opened, click on cancel button and Do Not delete the row
            :param close:  if provided, after the popup is opened, click on close button and Do Not delete the row
            :return: Bool Returns true if successful or returns the string of the delete prompt if looking for prompt message
        """

        # Click on action
        with self.wait_stale():
            _row = self._get_row(name)
            _row.find_element(*list(self.elements["delete"]._asdict().values())).click()

            self.wait_for("delete_prompt")
            if cancel:
                self.wait_to_be_clickable("delete_cancel")
                self.delete_cancel.click()
                self.wait_until("delete_cancel")
                return True
            elif close:
                self.wait_to_be_clickable("delete_close")
                self.delete_close.click()
                self.wait_until("delete_close")
                return True
            elif prompt_msg:
                self.wait_for_text("delete_prompt")
                return self.get_clear_text(self.delete_prompt)
            else:
                self.wait_to_be_clickable("delete_btn")
                self.delete_btn.click()
                self.wait_for("app_listings")

    def set_filter(self, filter_query):
        """
        Provide a string in table filter.
            :param filter_query: query of the filter
            :returns: resultant list of filtered row_names
        """
        with self.wait_stale():
            self.filter.clear()
            self.filter.send_keys(filter_query)
            self._wait_for_loadspinner()
        return self.get_column_values("name")

    @contextmanager
    def wait_stale(self):
        rows = list(self._get_rows())
        col = copy.deepcopy(self.elements["col"])
        col = col._replace(select=col.select.format(column="name"))
        col_element = self._get_element(col.by, col.select)
        yield
        if len(rows) > 0 and self.wait_to_be_stale(rows[0]):
            self.wait_to_be_stale(col_element)

    def clean_filter(self):
        """
        Clean the filter textbox
        """
        self.filter.clear()
        self._wait_for_loadspinner()

    def _get_column_value(self, row, column):
        """
        Get the column from a specific row provided.
            :param row: the webElement of the row
            :param column: the header name of the column
            :return: The list of column values from a specific column and row
        """
        find_by_col_number = False
        if column.lower().replace(" ", "_") in self.header_mapping:
            column = self.header_mapping[column.lower().replace(" ", "_")]
            find_by_col_number = isinstance(column, int)
        else:
            column = column.lower().replace(" ", "_")

        if not find_by_col_number:
            col = copy.deepcopy(self.elements["col"])
            col = col._replace(select=col.select.format(column=column))
            self.wait_for("app_listings")
            return self.get_clear_text(row.find_element(*list(col._asdict().values())))
        else:
            # Int value
            col = copy.deepcopy(self.elements["col-number"])
            col = col._replace(select=col.select.format(col_number=column))
            self.wait_for("app_listings")
            return self.get_clear_text(row.find_element(*list(col._asdict().values())))

    def _get_rows(self):
        """
        Get list of rows
            :return: The list of rows within the table
        """
        yield from self.get_elements("rows")

    def _get_row(self, name):
        """
        Get the specified row.
        :param name: row name
            :return: element Gets the row specified within the table, or raises a warning if not found
        """
        for each_row in self._get_rows():
            if self._get_column_value(each_row, "name") == name:
                return each_row
        else:
            raise ValueError("{} row not found in table".format(name))

    def get_action_values(self, name):
        """
        Get the specified rows action values
            :param name: row name
            :return: List Gets the action values of the row specified within the table
        """
        _row = self._get_row(name)
        return [
            self.get_clear_text(each) for each in self.get_elements("action_values")
        ]

    def get_count_number(self):
        """
        Returns the count from the title of the table.
            :return: Int The title count of the table.
        """
        row_count = self.get_count_title()
        return int(re.search(r"\d+", row_count).group())

    def get_more_info(self, name, cancel=True):
        """
        Returns the text from the more info field within a tables row
            :param name: Str row name
            :param cancel: Bool Whether or not to click cancel after getting the info
            :return: Dict The information found when opening the info table on a row in the table
        """
        _row = self._get_row(name)
        _row.find_element(*list(self.elements["more_info"]._asdict().values())).click()
        keys = self.more_info_row.find_elements(
            *list(self.elements["more_info_key"]._asdict().values())
        )
        values = self.more_info_row.find_elements(
            *list(self.elements["more_info_value"]._asdict().values())
        )
        more_info = {
            self.get_clear_text(key): self.get_clear_text(value)
            for key, value in zip(keys, values)
        }

        if cancel:
            _row = self._get_row(name)
            _row.find_element(
                *list(self.elements["more_info"]._asdict().values())
            ).click()

        return more_info

    def switch_to_page(self, value):
        """
        Switches the table to specified page
            :param value: Int The page to switch the table to
            :return: Bool whether or not switching to the page was successful
        """
        for each in self.get_elements("switch_to_page"):
            if self.get_clear_text(each).lower() not in [
                "prev",
                "next",
            ] and self.get_clear_text(each) == str(value):
                each.click()
                return True
        else:
            raise ValueError("{} not found".format(value))

    def switch_to_prev(self):
        """
        Switches the table's page back by 1
            :return: Bool whether or not switching to the previous page was successful
        """
        for page_prev in self.get_elements("switch_to_page"):
            if self.get_clear_text(page_prev).lower() == "prev":
                page_prev.click()
                return True
        else:
            raise ValueError("{} not found".format(page_prev))

    def switch_to_next(self):
        """
        Switches the table's page forward by 1
            :return: Bool whether or not switching to the next page was successful
        """
        for page_next in self.get_elements("switch_to_page"):
            if self.get_clear_text(page_next).lower() == "next":
                page_next.click()
                return True
        else:
            raise ValueError("{} not found".format(page_next))

    def check_alert_sign(self, row_name, column_name="account"):
        """
        This function check account warning present in the table while account is not configured in input
            :param row_name: the name of the row
            :param column_name: the header name of the column
        """
        column_selector = column_name.lower().replace(" ", "_")
        column_selector = self.header_mapping.get(column_selector, column_name)

        col = copy.deepcopy(self.elements["alert_sign"])
        col = col._replace(select=col.select.format(column=column_selector))

        _row = self._get_row(row_name)
        try:
            _row.find_element(*list(col._asdict().values()))
            return True
        except exceptions.NoSuchElementException:
            return False
