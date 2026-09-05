from unittest.mock import MagicMock

from selenium.common.exceptions import StaleElementReferenceException

from pytest_splunk_addon_ui_smartx.components.base_component import Selector
from pytest_splunk_addon_ui_smartx.components.table import Table


def _poll_twice(condition, **_kwargs):
    for _ in range(2):
        result = condition(MagicMock())
        if result:
            return result
    raise AssertionError("condition did not succeed on the refreshed DOM")


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
    assert browser.execute_script.call_args[0][1:] == (
        row,
        "test_kinesis_clone",
        {"input_name": "name", "status": "disabled"},
    )


def test_get_table_row_supports_positional_header_mapping():
    expected = {"input type": "Amazon SQS"}
    browser = MagicMock()
    browser.execute_script.return_value = expected
    row = MagicMock()
    table = Table(
        browser,
        Selector(select='[data-test="table"]'),
        mapping={"input_type": 3},
    )
    table.get_elements = MagicMock(return_value=[row])

    assert table.get_table_row("test_sqs_input") == expected
    (
        snapshot_script,
        snapshot_row,
        row_name,
        mapping,
    ) = browser.execute_script.call_args[0]
    assert "Number.isInteger(dataColumn)" in snapshot_script
    assert "row.querySelector(`td:nth-child(${dataColumn})`)" in snapshot_script
    assert (snapshot_row, row_name, mapping) == (
        row,
        "test_sqs_input",
        {"input_type": 3},
    )


def test_get_table_row_reacquires_rows_after_stale_snapshot():
    expected = {"input name": "test_kinesis_input", "status": "Active"}
    browser = MagicMock()
    browser.execute_script.side_effect = [
        StaleElementReferenceException("table refreshed"),
        expected,
    ]
    stale_row = MagicMock()
    refreshed_row = MagicMock()
    table = Table(browser, Selector(select='[data-test="table"]'))
    table._get_rows = MagicMock(side_effect=[iter([stale_row]), iter([refreshed_row])])
    table.wait_for = MagicMock(side_effect=_poll_twice)

    assert table.get_table_row("test_kinesis_input") == expected
    assert table._get_rows.call_count == 2


def test_get_row_reacquires_table_after_stale_lookup():
    stale_row = MagicMock()
    refreshed_row = MagicMock()
    table = Table(MagicMock(), Selector(select='[data-test="table"]'))
    table._get_rows = MagicMock(side_effect=[iter([stale_row]), iter([refreshed_row])])
    table._get_column_value = MagicMock(
        side_effect=[
            StaleElementReferenceException("table refreshed"),
            "test_billing_input",
        ]
    )
    table.wait_for = MagicMock(side_effect=_poll_twice)

    assert table._get_row("test_billing_input") is refreshed_row
    assert table._get_rows.call_count == 2
