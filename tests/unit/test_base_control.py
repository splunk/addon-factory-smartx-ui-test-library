from unittest.mock import MagicMock

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
    screen_reader_content = MagicMock()
    screen_reader_content.get_attribute.return_value = "(Opens new window)"

    def get_element(key):
        if control.elements[key].select == '[data-test="popover"]':
            return visible_popover
        return screen_reader_content

    control.get_element = MagicMock(side_effect=get_element)

    assert control.get_tooltip_text() == expected
