import pytest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from pytest_splunk_addon_ui_smartx.components.table import Table


@pytest.fixture
def mock_table():
    mock_browser = MagicMock()

    # Mocking container with a `select` attribute
    mock_container = MagicMock()
    mock_container.select = "#test-container"
    table = Table(mock_browser, mock_container)
    return table


@patch("pytest_splunk_addon_ui_smartx.components.table.Table._get_row")
def test_get_more_info_expand_row_false(mock_get_row, mock_table):
    mock_row = MagicMock()
    mock_get_row.return_value = mock_row

    mock_more_info_element = MagicMock()
    mock_row.find_element.return_value = mock_more_info_element

    # Calling the function with expand_row=False and cancel=False as we are testing for expand_row parameter
    mock_table.get_more_info(name="Test Row", cancel=False, expand_row=False)

    mock_get_row.assert_called_with("Test Row")
    mock_row.find_element.assert_not_called()
    mock_more_info_element.click.assert_not_called()


@patch("pytest_splunk_addon_ui_smartx.components.table.Table._get_row")
def test_get_more_info_expand_row_true(mock_get_row, mock_table):
    mock_row = MagicMock()
    mock_get_row.return_value = mock_row

    mock_more_info_element = MagicMock()
    mock_row.find_element.return_value = mock_more_info_element

    mock_key1 = MagicMock()
    mock_key1.get_attribute.return_value = "  Key1  "
    mock_key2 = MagicMock()
    mock_key2.get_attribute.return_value = "  Key2  "

    mock_value1 = MagicMock()
    mock_value1.get_attribute.return_value = "  Value1  "
    mock_value2 = MagicMock()
    mock_value2.get_attribute.return_value = "  Value2  "

    mock_table.more_info_row.find_elements.side_effect = [
        [mock_key1, mock_key2],
        [mock_value1, mock_value2],
    ]

    # Call the function with expand_row=True and cancel=False as we are testing for expand_row parameter
    result = mock_table.get_more_info(name="Test Row", cancel=False, expand_row=True)

    mock_get_row.assert_called_with("Test Row")
    mock_more_info_element.click.assert_called_once()
    assert result == {"Key1": "Value1", "Key2": "Value2"}
