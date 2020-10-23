# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ...components.table import Table
from ...components.base_component import Selector


class AlertTable(Table):
    def __init__(self, browser):
        container = Selector(select='.grid-placeholder')
        super(AlertTable, self).__init__(browser, container)
        self.elements.update({
            "rows": Selector(select=container.select + " tr.list-item.savedsearches-gridrow"),
            "header": Selector(select=container.select + " th"),
            "col": Selector(select=container.select + " td.cell-{column}"),
            "app_listings": Selector(select=container.select + " tbody"),
        })
