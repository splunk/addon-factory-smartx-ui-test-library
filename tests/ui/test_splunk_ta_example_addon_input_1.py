from pytest_splunk_addon_ui_smartx.base_test import UccTester
from pytest_splunk_addon_ui_smartx.utils import get_browser_logs, LogLevel, LogSource
from .Example_UccLib.account import AccountPage
from .Example_UccLib.input_page import InputPage
import pytest


@pytest.fixture(scope="module", autouse=True)
def add_account(ucc_smartx_rest_helper):
    account = AccountPage(
        ucc_smartx_rest_helper=ucc_smartx_rest_helper, open_page=False
    )
    url = account._get_account_endpoint()
    kwargs = {
        "name": "test_input",
        "account_checkbox": 1,
        "account_multiple_select": "one",
        "account_radio": "yes",
        "auth_type": "basic",
        "custom_endpoint": "login.example.com",
        "username": "TestUser",
        "password": "TestPassword",
        "token": "TestToken",
        "client_id": "",
        "client_secret": "",
        "redirect_url": "",
        "endpoint": "",
        "example_help_link": "",
    }
    yield account.backend_conf.post_stanza(url, kwargs)
    account.backend_conf.delete_all_stanzas()


@pytest.fixture
def add_multiple_inputs(ucc_smartx_rest_helper):
    input_page = InputPage(
        ucc_smartx_rest_helper=ucc_smartx_rest_helper, open_page=False
    )
    url = input_page._get_input_endpoint()
    for i in range(50):
        kwargs = {
            "name": "example_input_one://dummy_input_one" + str(i),
            "account": "test_input",
            "input_one_checkbox": "1",
            "input_one_radio": "yes",
            "interval": "90",
            "limit": "1000",
            "multipleSelectTest": "a|b",
            "object": "test_object",
            "object_fields": "test_field",
            "order_by": "LastModifiedDate",
            "singleSelectTest": "two",
            "start_date": "2020-12-11T20:00:32.000z",
            "disabled": 0,
        }
        input_page.backend_conf.post_stanza(url, kwargs)
        kwargs = {
            "name": "example_input_two://dummy_input_two" + str(i),
            "account": "test_input",
            "input_two_checkbox": "1",
            "input_two_radio": "no",
            "interval": "100",
            "input_two_multiple_select": "one,two",
            "index": "main",
            "start_date": "2016-10-10T12:10:15.000z",
            "disabled": 0,
        }
        input_page.backend_conf.post_stanza(url, kwargs)


@pytest.fixture
def add_input_one(ucc_smartx_rest_helper):
    input_page = InputPage(
        ucc_smartx_rest_helper=ucc_smartx_rest_helper, open_page=False
    )
    url = input_page._get_input_endpoint()
    kwargs = {
        "name": "example_input_one://dummy_input_one",
        "account": "test_input",
        "input_one_checkbox": "1",
        "input_one_radio": "yes",
        "interval": "90",
        "limit": "1000",
        "multipleSelectTest": "a|b",
        "object": "test_object",
        "object_fields": "test_field",
        "order_by": "LastModifiedDate",
        "singleSelectTest": "two",
        "start_date": "2020-12-11T20:00:32.000z",
        "disabled": 0,
        "example_textarea_field": "line1\nline2",
    }
    yield input_page.backend_conf.post_stanza(url, kwargs)


@pytest.fixture
def add_input_two(ucc_smartx_rest_helper):
    input_page = InputPage(
        ucc_smartx_rest_helper=ucc_smartx_rest_helper, open_page=False
    )
    url = input_page._get_input_endpoint()
    kwargs = {
        "name": "example_input_two://dummy_input_two",
        "account": "test_input",
        "input_two_checkbox": "1",
        "input_two_radio": "no",
        "interval": "100",
        "input_two_multiple_select": "one,two",
        "index": "main",
        "start_date": "2016-10-10T12:10:15.000z",
        "disabled": 0,
    }
    yield input_page.backend_conf.post_stanza(url, kwargs)


@pytest.fixture(autouse=True)
# All the inputs created should start with dummy_input as prefix
def delete_inputs(ucc_smartx_rest_helper):
    yield
    input_page = InputPage(
        ucc_smartx_rest_helper=ucc_smartx_rest_helper, open_page=False
    )
    input_page.backend_conf.delete_all_stanzas("search=dummy_input")


class TestInput(UccTester):
    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_required_field_name(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field name in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.example_radio.select("Yes")
        input_page.entity1.single_select_group_test.select("two")
        input_page.entity1.interval.set_value("90")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity1.save,
            r"Field Name is required",
            left_args={"expect_error": True},
        )

        severe_console_logs = get_browser_logs(
            ucc_smartx_selenium_helper.browser,
            log_level=LogLevel.SEVERE,
            log_source=LogSource.CONSOLE_API,
        )
        assert (
            not severe_console_logs
        ), f"Unexpected severe console logs found: {severe_console_logs}"

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_valid_length_name(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the name field should not be more than 100 characters"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        name_value = "a" * 101
        input_page.entity1.name.set_value(name_value)
        self.assert_util(
            input_page.entity1.save,
            r"Length of input name should be between 1 and 100",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_valid_input_name(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies whether adding special characters, name field displays validation error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("$$test_name")
        self.assert_util(
            input_page.entity1.save,
            r"Input Name must begin with a letter and consist exclusively of alphanumeric characters and underscores.",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_list_single_select_group_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies values Single Select Group Test dropdown in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        single_select_group_test_list = ["One", "Two", "Three", "Four"]
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(
            input_page.entity1.single_select_group_test.list_of_values(),
            single_select_group_test_list,
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_select_value_single_select_group_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies selected value of Single Select Group Test dropdown in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        selected_value = "Two"
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.single_select_group_test.select(selected_value)
        self.assert_util(
            input_page.entity1.single_select_group_test.get_value, selected_value
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_search_value_single_select_group_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies singleselect seach funtionality properly"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(
            input_page.entity1.single_select_group_test.search_get_list,
            ["one", "One"],
            left_args={"value": "one"},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_default_value_multiple_select_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default values of Multiple Select Test dropdown in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        default_values = ["A", "B"]
        self.assert_util(
            input_page.entity1.multiple_select_test.get_values, default_values
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_list_multiple_select_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies values of Multiple Select Test dropdown in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.multiple_select_test.deselect_all()
        multiple_select_test = ["A", "B"]
        self.assert_util(
            input_page.entity1.multiple_select_test.list_of_values(),
            multiple_select_test,
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_select_value_multiple_select_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies selected single value of Multiple Select Test dropdown in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        selected_value = ["A"]
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.multiple_select_test.deselect_all()
        for each in selected_value:
            input_page.entity1.multiple_select_test.select(each)
        self.assert_util(
            input_page.entity1.multiple_select_test.get_values, selected_value
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_select_multiple_values_multiple_select_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies selected multiple values of Multiple Select Test dropdown in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        selected_values = ["A", "B"]
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.multiple_select_test.deselect_all()
        for each in selected_values:
            input_page.entity1.multiple_select_test.select(each)
        self.assert_util(
            input_page.entity1.multiple_select_test.get_values, selected_values
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_deselect_multiple_select_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies deselect in Multiple Select Test dropdown in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        selected_values = ["A", "B"]
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.multiple_select_test.deselect_all()
        for each in selected_values:
            input_page.entity1.multiple_select_test.select(each)
        input_page.entity1.multiple_select_test.deselect("A")
        self.assert_util(input_page.entity1.multiple_select_test.get_values, ["B"])

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_search_value_multiple_select_test(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies multiple select seach funtionality properly"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.multiple_select_test.deselect_all()
        self.assert_util(
            input_page.entity1.multiple_select_test.search_get_list,
            ["A"],
            left_args={"value": "A"},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_default_value_example_checkbox(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default value of example checkbox in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(input_page.entity1.example_checkbox.is_checked, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_unchecked_example_checkbox(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies Uncheck in example checkbox in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.example_checkbox.check()
        self.assert_util(input_page.entity1.example_checkbox.uncheck, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_checked_example_checkbox(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies checked in example checkbox in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.example_checkbox.uncheck()
        self.assert_util(input_page.entity1.example_checkbox.check, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_default_value_example_radio(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default value of example radio in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(input_page.entity1.example_radio.get_value, "Yes")

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_select_value_example_radio(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies selected value of example radio in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.example_radio.select("No")
        self.assert_util(input_page.entity1.example_radio.get_value, "No")

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_required_field_interval(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field interval in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input")
        input_page.entity1.example_radio.select("Yes")
        input_page.entity1.single_select_group_test.select("Two")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity1.save,
            r"Field Interval is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_valid_input_interval(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies whether adding non numeric values, intreval field displays validation error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.name.set_value("test_name")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.interval.set_value("abc")
        self.assert_util(
            input_page.entity1.save,
            r"Interval must be either a non-negative number or -1.",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_required_field_index(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field index in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input")
        input_page.entity1.example_radio.select("Yes")
        input_page.entity1.single_select_group_test.select("Two")
        input_page.entity1.interval.set_value("90")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        input_page.entity1.index.cancel_selected_value()
        self.assert_util(
            input_page.entity1.save,
            r"Field Index is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_default_value_index(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default value of field index in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        default_index = "default"
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(input_page.entity1.index.get_value, default_index)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_required_field_example_account(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field Salesforce Account in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input")
        input_page.entity1.example_radio.select("Yes")
        input_page.entity1.single_select_group_test.select("Two")
        input_page.entity1.interval.set_value("90")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity1.save,
            r"Field Example Account is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_required_field_object(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field Object in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input")
        input_page.entity1.example_radio.select("Yes")
        input_page.entity1.single_select_group_test.select("Two")
        input_page.entity1.interval.set_value("90")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity1.save,
            r"Field Object is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_required_field_object_fields(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field Object Fields in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input")
        input_page.entity1.example_radio.select("Yes")
        input_page.entity1.single_select_group_test.select("Two")
        input_page.entity1.interval.set_value("90")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity1.save,
            r"Field Object Fields is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_required_field_order_by(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field Order By in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input")
        input_page.entity1.example_radio.select("Yes")
        input_page.entity1.interval.set_value("90")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.single_select_group_test.select("Two")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        input_page.entity1.order_by.set_value("")
        self.assert_util(
            input_page.entity1.save,
            r"Field Order By is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_default_value_order_by(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default value of field Order By in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        default_order_by = "LastModifiedDate"
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(input_page.entity1.order_by.get_value, default_order_by)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_fields_label_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies example input one field label"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        self.assert_util(input_page.entity1.name.get_input_label, "Name")
        self.assert_util(
            input_page.entity1.example_checkbox.get_input_label, "Example Checkbox"
        )
        self.assert_util(
            input_page.entity1.example_radio.get_input_label, "Example Radio"
        )
        self.assert_util(
            input_page.entity1.single_select_group_test.get_input_label,
            "Single Select Group Test",
        )
        self.assert_util(
            input_page.entity1.multiple_select_test.get_input_label,
            "Multiple Select Test",
        )
        self.assert_util(input_page.entity1.interval.get_input_label, "Interval")
        self.assert_util(input_page.entity1.index.get_input_label, "Index")
        self.assert_util(
            input_page.entity1.example_account.get_input_label, "Example Account"
        )
        self.assert_util(input_page.entity1.object.get_input_label, "Object")
        self.assert_util(
            input_page.entity1.object_fields.get_input_label, "Object Fields"
        )
        self.assert_util(input_page.entity1.order_by.get_input_label, "Order By")
        self.assert_util(
            input_page.entity1.query_start_date.get_input_label, "Query Start Date"
        )
        self.assert_util(input_page.entity1.limit.get_input_label, "Limit")

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_fields_label_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies example input two field label"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        self.assert_util(input_page.entity2.name.get_input_label, "Name")
        self.assert_util(input_page.entity2.interval.get_input_label, "Interval")
        self.assert_util(input_page.entity2.index.get_input_label, "Index")
        self.assert_util(
            input_page.entity2.example_account.get_input_label, "Example Account"
        )
        self.assert_util(
            input_page.entity2.example_multiple_select.get_input_label,
            "Example Multiple Select",
        )
        self.assert_util(
            input_page.entity2.example_checkbox.get_input_label, "Example Checkbox"
        )
        self.assert_util(
            input_page.entity2.example_radio.get_input_label, "Example Radio"
        )
        self.assert_util(
            input_page.entity2.query_start_date.get_input_label, "Query Start Date"
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_help_text_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies help text for the field name"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(
            input_page.entity1.name.get_help_text, "A unique name for the data input."
        )
        self.assert_util(
            input_page.entity1.example_checkbox.get_help_text,
            "This is an example checkbox for the input one entity",
        )
        self.assert_util(
            input_page.entity1.example_radio.get_help_text,
            "This is an example radio button for the input one entity",
        )
        self.assert_util(
            input_page.entity1.interval.get_help_text,
            "Time interval of the data input, in seconds.",
        )
        self.assert_util(
            input_page.entity1.object.get_help_text,
            "The name of the object to query for.",
        )
        self.assert_util(
            input_page.entity1.object_fields.get_help_text,
            "Object fields from which to collect data. Delimit multiple fields using a comma.",
        )
        self.assert_util(
            input_page.entity1.query_start_date.get_help_text,
            'The datetime after which to query and index records, in this format: "YYYY-MM-DDThh:mm:ss.000z". Defaults to 90 days earlier from now.',
        )
        self.assert_util(
            input_page.entity1.limit.get_help_text,
            "The maximum number of results returned by the query.",
        )
        self.assert_util(
            input_page.entity1.order_by.get_help_text,
            "The datetime field by which to query results in ascending order for indexing.",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_valid_input_query_start_date(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies whether adding wrong format, Query Start Date field displays validation error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("test_name")
        input_page.entity1.interval.set_value("120")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.object_fields.set_value("test_object_field")
        input_page.entity1.query_start_date.set_value("2020/01/01")
        self.assert_util(
            input_page.entity1.save,
            r"Invalid date and time format",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_default_value_limit(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default value of field limit in example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        default_limit = "1000"
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(input_page.entity1.limit.get_value, default_limit)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_help_link(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies whether the help link redirects to the correct URL"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        go_to_link = "https://docs.splunk.com/Documentation"
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        with input_page.entity1.help_link.open_link() as link_url:
            self.assert_util(input_page.entity1.help_link.get_current_url, go_to_link)

    ###################################
    #### TEST CASES FOR ENTITY ONE ####
    ###################################

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_one_add_frontend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the frontend after adding a Example Input One"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input")
        input_page.entity1.example_radio.select("Yes")
        input_page.entity1.single_select_group_test.select("Two")
        input_page.entity1.interval.set_value("90")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        input_page.entity1.text_area.set_value("line1\nline2")
        self.assert_util(input_page.entity1.save, True)
        input_page.table.wait_for_rows_to_appear(1)
        self.assert_util(
            input_page.table.get_table()["dummy_input"],
            {
                "name": "dummy_input",
                "account": "test_input",
                "interval": "90",
                "index": "default",
                "status": "Enabled",
                "actions": "Edit | Clone | Delete",
            },
        )

        url = input_page._get_input_endpoint()

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_one_add_backend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the backend after adding a example input one"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input")
        input_page.entity1.example_radio.select("No")
        input_page.entity1.single_select_group_test.select("Two")
        input_page.entity1.interval.set_value("90")
        input_page.entity1.example_account.select("test_input")
        input_page.entity1.object.set_value("test_object")
        input_page.entity1.object_fields.set_value("test_field")
        input_page.entity1.query_start_date.set_value("2020-12-11T20:00:32.000z")
        input_page.entity1.text_area.set_value("line1\nline2")
        self.assert_util(input_page.entity1.save, True)
        input_page.table.wait_for_rows_to_appear(1)
        value_to_test = {
            "account": "test_input",
            "input_one_checkbox": "1",
            "input_one_radio": "0",
            "interval": "90",
            "limit": "1000",
            "multipleSelectTest": "a|b",
            "object": "test_object",
            "object_fields": "test_field",
            "order_by": "LastModifiedDate",
            "singleSelectTest": "two",
            "start_date": "2020-12-11T20:00:32.000z",
            "disabled": 0,
            "example_textarea_field": "line1\nline2",
        }
        backend_stanza = input_page.backend_conf.get_stanza(
            "example_input_one://dummy_input"
        )
        for each_key, each_value in value_to_test.items():
            assert each_key in backend_stanza
            self.assert_util(
                each_value,
                backend_stanza[each_key],
            )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_edit_uneditable_field_name(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the frontend uneditable fields at time of edit of the example input one entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        self.assert_util(input_page.entity1.name.is_editable, False)
        self.assert_util(input_page.entity1.single_select_group_test.is_editable, False)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_one_edit_frontend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the frontend edit functionality of the example input one entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        input_page.entity1.example_checkbox.uncheck()
        input_page.entity1.example_radio.select("No")
        input_page.entity1.multiple_select_test.deselect("b")
        input_page.entity1.interval.set_value("3600")
        input_page.entity1.index.select("main")
        input_page.entity1.object.set_value("edit_object")
        input_page.entity1.object_fields.set_value("edit_field")
        input_page.entity1.order_by.set_value("LastDate")
        input_page.entity1.limit.set_value("2000")
        input_page.entity1.query_start_date.set_value("2020-20-20T20:20:20.000z")
        input_page.entity1.text_area.set_value("line3\nline4")
        self.assert_util(input_page.entity1.save, True)
        input_page.table.wait_for_rows_to_appear(1)
        self.assert_util(
            input_page.table.get_table()["dummy_input_one"],
            {
                "name": "dummy_input_one",
                "account": "test_input",
                "interval": "3600",
                "index": "main",
                "status": "Enabled",
                "actions": "Edit | Clone | Delete",
            },
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_one_edit_backend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the backend edit functionality of the example input one entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        input_page.entity1.example_checkbox.uncheck()
        input_page.entity1.example_radio.select("No")
        input_page.entity1.multiple_select_test.deselect("b")
        input_page.entity1.interval.set_value("3600")
        input_page.entity1.index.select("main")
        input_page.entity1.object.set_value("edit_object")
        input_page.entity1.object_fields.set_value("edit_field")
        input_page.entity1.order_by.set_value("LastDate")
        input_page.entity1.limit.set_value("2000")
        input_page.entity1.query_start_date.set_value("2020-20-20T20:20:20.000z")
        input_page.entity1.text_area.set_value("line3\nline4")
        self.assert_util(input_page.entity1.save, True)
        input_page.table.wait_for_rows_to_appear(1)
        value_to_test = {
            "account": "test_input",
            "input_one_checkbox": "0",
            "input_one_radio": "0",
            "interval": "3600",
            "index": "main",
            "limit": "2000",
            "multipleSelectTest": "a",
            "object": "edit_object",
            "object_fields": "edit_field",
            "order_by": "LastDate",
            "singleSelectTest": "two",
            "start_date": "2020-20-20T20:20:20.000z",
            "disabled": 0,
            "example_textarea_field": "line3\nline4",
        }
        backend_stanza = input_page.backend_conf.get_stanza(
            "example_input_one://dummy_input_one"
        )
        for each_key, each_value in value_to_test.items():
            self.assert_util(each_value, backend_stanza[each_key])

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_clone_default_values(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the frontend default fields at time of clone for example input one entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_one")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(input_page.entity1.name.get_value, "")
        self.assert_util(input_page.entity1.example_checkbox.is_checked, True)
        self.assert_util(input_page.entity1.example_radio.get_value, "Yes")
        self.assert_util(input_page.entity1.single_select_group_test.get_value, "Two")
        self.assert_util(input_page.entity1.multiple_select_test.get_values, ["A", "B"])
        self.assert_util(input_page.entity1.interval.get_value, "90")
        self.assert_util(input_page.entity1.index.get_value, "default")
        self.assert_util(input_page.entity1.example_account.get_value, "test_input")
        self.assert_util(input_page.entity1.object.get_value, "test_object")
        self.assert_util(input_page.entity1.object_fields.get_value, "test_field")
        self.assert_util(input_page.entity1.order_by.get_value, "LastModifiedDate")
        self.assert_util(
            input_page.entity1.query_start_date.get_value, "2020-12-11T20:00:32.000z"
        )
        self.assert_util(input_page.entity1.limit.get_value, "1000")
        self.assert_util(input_page.entity1.text_area.get_value, "line1\nline2")

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_one_clone_frontend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the frontend clone functionality of the example input one entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.wait_for_rows_to_appear(1)
        input_page.table.clone_row("dummy_input_one")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input_one_Clone_Test")
        input_page.entity1.interval.set_value("180")
        input_page.entity1.limit.set_value("500")
        input_page.entity1.text_area.set_value("line1\nline2")
        self.assert_util(input_page.entity1.save, True)
        input_page.table.wait_for_rows_to_appear(2)
        self.assert_util(
            input_page.table.get_table()["dummy_input_one_Clone_Test"],
            {
                "name": "dummy_input_one_Clone_Test",
                "account": "test_input",
                "interval": "180",
                "index": "default",
                "status": "Enabled",
                "actions": "Edit | Clone | Delete",
            },
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_one_clone_backend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the backend clone functionality of the example input one entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.wait_for_rows_to_appear(1)
        input_page.table.clone_row("dummy_input_one")
        input_page.entity1.example_account.wait_for_values()
        input_page.entity1.name.set_value("dummy_input_one_Clone_Test")
        input_page.entity1.interval.set_value("180")
        input_page.entity1.limit.set_value("500")
        input_page.entity1.text_area.set_value("line3\nline4")
        self.assert_util(input_page.entity1.save, True)
        input_page.table.wait_for_rows_to_appear(2)
        value_to_test = {
            "account": "test_input",
            "input_one_checkbox": "1",
            "input_one_radio": "1",
            "interval": "180",
            "index": "default",
            "limit": "500",
            "multipleSelectTest": "a|b",
            "object": "test_object",
            "object_fields": "test_field",
            "order_by": "LastModifiedDate",
            "singleSelectTest": "two",
            "start_date": "2020-12-11T20:00:32.000z",
            "disabled": 0,
            "example_textarea_field": "line3\nline4",
        }
        backend_stanza = input_page.backend_conf.get_stanza(
            "example_input_one://dummy_input_one_Clone_Test"
        )
        for each_key, each_value in value_to_test.items():
            self.assert_util(each_value, backend_stanza[each_key])

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_one_delete_row_frontend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the frontend delete functionlity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.input_status_toggle("dummy_input_one", enable=False)
        input_page.table.delete_row("dummy_input_one")
        input_page.table.wait_for_rows_to_appear(0)
        self.assert_util("dummy_input_one", input_page.table.get_table, "not in")

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_one_delete_row_backend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the backend delete functionlity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.input_status_toggle("dummy_input_one", enable=False)
        input_page.table.delete_row("dummy_input_one")
        input_page.table.wait_for_rows_to_appear(0)
        self.assert_util(
            "example_input_one://dummy_input_one",
            input_page.backend_conf.get_all_stanzas().keys(),
            "not in",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_add_close_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies close functionality at time of add"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(input_page.entity1.close, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_edit_close_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies close functionality at time of edit"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        self.assert_util(input_page.entity1.close, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_clone_close_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies close functionality at time of clone"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_one")
        self.assert_util(input_page.entity1.close, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_delete_close_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies close functionality at time of delete"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(
            input_page.table.delete_row,
            True,
            left_args={"name": "dummy_input_one", "close": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_add_cancel_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies cancel functionality at time of add"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(input_page.entity1.cancel, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_edit_cancel_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies cancel functionality at time of edit"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        self.assert_util(input_page.entity1.cancel, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_clone_cancel_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies cancel functionality at time of clone"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_one")
        self.assert_util(input_page.entity1.cancel, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_delete_cancel_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies cancel functionality at time of delete"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(
            input_page.table.delete_row,
            True,
            left_args={"name": "dummy_input_one", "cancel": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_add_duplicate_names(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies by saving an entity with duplicate name it displays and error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        input_name = "dummy_input_one"
        input_page.entity1.name.set_value(input_name)
        self.assert_util(
            input_page.entity1.save,
            "Name {} is already in use".format(input_name),
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_clone_duplicate_names(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies by saving an entity with duplicate name at time of clone it displays and error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_one")
        input_page.entity1.example_account.wait_for_values()
        input_name = "dummy_input_one"
        input_page.entity1.name.set_value(input_name)
        self.assert_util(
            input_page.entity1.save,
            "Name {} is already in use".format(input_name),
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_add_valid_title(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the title of the 'Add Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        input_page.entity1.example_account.wait_for_values()
        self.assert_util(
            input_page.entity1.title.container.get_attribute("textContent").strip(),
            "Add Example Input One",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_edit_valid_title(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the title of the 'Edit Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        self.assert_util(
            input_page.entity1.title.container.get_attribute("textContent").strip(),
            "Update Example Input One",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_clone_valid_title(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the title of the 'Clone Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_one")
        self.assert_util(
            input_page.entity1.title.container.get_attribute("textContent").strip(),
            "Clone Example Input One",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_delete_valid_title(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the title of the 'Delete Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.delete_row("dummy_input_one", prompt_msg=True)
        self.assert_util(
            input_page.entity1.title.container.get_attribute("textContent").strip(),
            "Delete Confirmation",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_one_delete_valid_prompt_message(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the prompt message of the 'Delete Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_name = "dummy_input_one"
        prompt_message = input_page.table.delete_row("dummy_input_one", prompt_msg=True)
        self.assert_util(
            prompt_message, 'Are you sure you want to delete "{}" ?'.format(input_name)
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_textarea_height(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """
        Verifies that textarea height values
        """
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        min_textarea_height = 71
        max_textarea_height = 311
        long_input = ""
        self.assert_util(
            min_textarea_height, input_page.entity1.text_area.get_textarea_height
        )
        for i in range(1, 50):
            long_input += f"{str(i)}\n"
        input_page.entity1.text_area.append_value(long_input)
        self.assert_util(
            max_textarea_height, input_page.entity1.text_area.get_textarea_height
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_textarea_big_input(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """
        Verifies that textarea can handle big inputs
        """
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        big_input = ""
        for i in range(1, 1000):
            big_input += f"{str(i)}\n"
        input_page.entity1.text_area.set_value(big_input)
        self.assert_util(big_input, input_page.entity1.text_area.get_value())
        self.assert_util(input_page.entity1.save, True)
        input_page.table.edit_row("dummy_input_one")
        self.assert_util(big_input.strip(), input_page.entity1.text_area.get_value())

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_textarea_scroll(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """
        Verifies that textarea height values
        """
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        long_input = ""
        screnshot_before = input_page.entity1.text_area.screenshot()
        for i in range(1, 50):
            long_input += f"{str(i)}\n"
        input_page.entity1.text_area.append_value(long_input)
        input_page.entity1.text_area.scroll("UP", 40)
        screenshot_after = input_page.entity1.text_area.screenshot()
        self.assert_util(screnshot_before, screenshot_after, operator="!=")

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_single_select_allows_new_values(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """
        Verifies that SingleSelect value is editable or not
        """
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input One")
        self.assert_util(
            input_page.entity1.single_select_group_test.allow_new_values, True
        )
        self.assert_util(input_page.entity1.index.allow_new_values, True)
        self.assert_util(input_page.entity1.example_account.allow_new_values, False)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_single_select_is_editable(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """
        Verifies that SingleSelect value is editable or not
        """
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_one")
        self.assert_util(input_page.entity1.example_account.is_editable, False)
        self.assert_util(input_page.entity1.index.is_editable, True)
