from unittest.mock import MagicMock

from pytest_splunk_addon_ui_smartx.components.base_component import Selector
from pytest_splunk_addon_ui_smartx.components.table import Table


def test_get_table_row_returns_atomic_visible_row_snapshot():
    expected = {
        "input name": "test_kinesis_clone",
        "status": "Active",
        "actions": "Edit | Clone | Delete",
    }
    browser = MagicMock()
    browser.execute_script.return_value = expected
    row = MagicMock()
    table = Table(
        browser,
        Selector(select='[data-test="table"]'),
        mapping={"input_name": "name", "status": "disabled"},
    )
    table.get_elements = MagicMock(return_value=[row])

    assert table.get_table_row("test_kinesis_clone") == expected
    browser.execute_script.assert_called_once()
    assert browser.execute_script.call_args.args[1:] == (
        row,
        "test_kinesis_clone",
        {"input_name": "name", "status": "disabled"},
    )
