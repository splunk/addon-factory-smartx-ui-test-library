from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

from pytest_splunk_addon_ui_smartx.base_test import UccTester


@pytest.fixture()
def ucc_mock():
    ucc = UccTester()
    ucc.wait = MagicMock()

    def f(x):
        out = x("fake_browser")
        if out:
            return out
        raise TimeoutException

    ucc.wait.until.side_effect = f
    return ucc


@pytest.mark.parametrize(
    "left, right, operator",
    [
        (lambda x: x, lambda x: x, "=="),
        (lambda x: x, lambda x: not x, "!="),
        (lambda x: -x, lambda x: x, "<"),
        (lambda x: -x, lambda x: x, "<="),
        (lambda x: x, lambda x: x, "<="),
        (lambda x: x, lambda x: -x, ">"),
        (lambda x: x, lambda x: -x, ">="),
        (lambda x: x, lambda x: x, ">="),
        (lambda x: x, lambda x: [x, 1, 2], "in"),
        (lambda x: x, [], "not in"),
        (lambda x: x, lambda x: x, "is"),
        (lambda x: x, lambda x: not x, "is not"),
    ],
)
def test_operator_map_callable_obj_pass(ucc_mock, left, right, operator):
    args = {"x": 1}
    ucc_mock.assert_util(left, right, operator, args, args)


@pytest.mark.parametrize(
    "left, right, operator",
    [
        (lambda x: x, lambda x: -x, "=="),
        (lambda x: x, lambda x: x, "!="),
        (lambda x: x, lambda x: x, "<"),
        (lambda x: x, lambda x: -x, "<"),
        (lambda x: x, lambda x: -x, "<="),
        (lambda x: x, lambda x: x, ">"),
        (lambda x: -x, lambda x: x, ">"),
        (lambda x: -x, lambda x: x, ">="),
        (lambda x: x, lambda x: [], "in"),
        (lambda x: x, lambda x: [x, 1, 2], "not in"),
        (lambda x: x, lambda x: not x, "is"),
        (lambda x: x, lambda x: x, "is not"),
    ],
)
def test_operator_map_callable_obj_assert_error(ucc_mock, left, right, operator):
    args = {"x": 1}
    with pytest.raises(AssertionError):
        ucc_mock.assert_util(left, right, operator, args, args)


@pytest.mark.parametrize(
    "left,right,operator",
    [
        (2, 2, "=="),
        ("a", "a", "=="),
        (True, True, "=="),
        (None, None, "=="),
        (1, 2, "!="),
        ("a", "b", "!="),
        (None, "a", "!="),
        (True, False, "!="),
        (1, 2, "<"),
        (False, True, "<"),
        ("a", "b", "<"),
        (1, 2, "<="),
        (2, 2, "<="),
        (False, True, "<="),
        (True, True, "<="),
        ("a", "b", "<="),
        ("a", "a", "<="),
        (2, 1, ">"),
        ("b", "a", ">"),
        (True, False, ">"),
        (2, 1, ">="),
        (1, 1, ">="),
        ("b", "a", ">="),
        (True, False, ">="),
        ("a", "a", ">="),
        (False, False, ">="),
        (1, [1, 2, 3], "in"),
        ("1", "123", "in"),
        (1, [2, 3], "not in"),
        ("1", "", "not in"),
        (1, 1, "is"),
        ("a", "a", "is"),
        (True, True, "is"),
        (None, None, "is"),
        (None, object, "is not"),
        (1, "a", "is not"),
        (1, 2, "is not"),
        ("a", "b", "is not"),
    ],
)
def test_operator_map_pass(ucc_mock, left, right, operator):
    ucc_mock.assert_util(left, right, operator)


@pytest.mark.parametrize(
    "left,right,operator",
    [
        (1, 2, "=="),
        ("a", "b", "=="),
        (True, False, "=="),
        (None, 1, "=="),
        (1, 1, "!="),
        ("a", "a", "!="),
        (None, None, "!="),
        (True, True, "!="),
        (1, 1, "<"),
        (False, False, "<"),
        ("a", "a", "<"),
        (2, 1, "<="),
        (True, False, "<="),
        ("b", "a", "<="),
        (1, 2, ">"),
        ("a", "b", ">"),
        (False, True, ">"),
        (1, 2, ">="),
        ("a", "b", ">="),
        (False, True, ">="),
        (1, [2, 3], "in"),
        ("1", "23", "in"),
        (1, [1, 2, 3], "not in"),
        ("1", "12", "not in"),
        (1, 2, "is"),
        ("a", "b", "is"),
        (True, False, "is"),
        (object, None, "is"),
        (None, None, "is not"),
        (1, 1, "is not"),
        ("a", "a", "is not"),
    ],
)
def test_operator_map_assert_error(ucc_mock, left, right, operator):
    with pytest.raises(AssertionError):
        ucc_mock.assert_util(left, right, operator)


@pytest.mark.parametrize(
    "exception", [TimeoutException, ElementNotInteractableException]
)
def test_exeption_in_assert_util(ucc_mock, exception):
    with patch("builtins.callable", side_effect=exception("important msg")):
        with pytest.raises(Exception, match="important msg"):
            ucc_mock.assert_util("left", "right")
