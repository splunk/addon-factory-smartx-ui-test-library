from unittest.mock import MagicMock

from selenium.common.exceptions import TimeoutException

from pytest_splunk_addon_ui_smartx.components.base_component import Selector
from pytest_splunk_addon_ui_smartx.components.controls.base_control import BaseControl


def test_get_tooltip_text_returns_visible_popover_without_screen_reader_text():
    expected = "A regular expression used to filter reports by name."
    browser = MagicMock()
    control = BaseControl(browser, Selector(select='[data-name="report_names"]'))
    control.hover_over_element = MagicMock()
    control.wait_for = MagicMock()

    visible_popover = MagicMock()
    visible_popover.text = expected
    visible_popover.get_attribute.return_value = expected + " (Opens new window)"
    control.wait_for.return_value = visible_popover

    assert control.get_tooltip_text() == expected


def test_get_tooltip_text_falls_back_to_visible_legacy_tooltip():
    expected = "Legacy tooltip content"
    browser = MagicMock()
    control = BaseControl(browser, Selector(select='[data-name="legacy_field"]'))
    control.hover_over_element = MagicMock()

    legacy_tooltip = MagicMock()
    legacy_tooltip.text = expected
    control.wait_for = MagicMock(
        side_effect=[TimeoutException("modern tooltip absent"), legacy_tooltip]
    )

    assert control.get_tooltip_text() == expected


def test_get_tooltip_text_skips_empty_visible_tooltip_before_fallback():
    expected = "Legacy tooltip content"
    browser = MagicMock()
    control = BaseControl(browser, Selector(select='[data-name="legacy_field"]'))
    control.hover_over_element = MagicMock()

    empty_popover = MagicMock()
    empty_popover.text = "  "
    legacy_tooltip = MagicMock()
    legacy_tooltip.text = expected
    control.wait_for = MagicMock(side_effect=[empty_popover, legacy_tooltip])

    assert control.get_tooltip_text() == expected


def test_get_tooltip_text_falls_back_to_screen_reader_content_scoped_to_control():
    expected = "Accessible tooltip content"
    browser = MagicMock()
    container = Selector(select='[data-name="accessible_field"]')
    control = BaseControl(browser, container)
    control.hover_over_element = MagicMock()

    accessible_tooltip = MagicMock()
    accessible_tooltip.get_attribute.return_value = expected
    control.wait_for = MagicMock(
        side_effect=[
            TimeoutException("modern tooltip absent"),
            TimeoutException("legacy tooltip absent"),
            accessible_tooltip,
        ]
    )

    assert control.get_tooltip_text() == expected
    assert control.elements["accessible_tooltip_text"].select == (
        container.select + ' [data-test="tooltip"] [data-test="screen-reader-content"]'
    )
