import time

from pytest_splunk_addon_ui_smartx.base_test import UccTester
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
        "apis": "ec2_volumes/3600,ec2_instances/100,classic_load_balancers/100",
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
    def test_example_input_two_required_field_name(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field name in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.example_checkbox.check()
        input_page.entity2.example_radio.select("No")
        input_page.entity2.example_multiple_select.select("Option One")
        input_page.entity2.index.select("main")
        input_page.entity2.interval.set_value("90")
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity2.save,
            r"Field Name is required",
            left_args={"expect_error": True},
        )
        input_page.entity2.name.set_value("test_name_two")
        self.assert_util(input_page.entity2.is_error_closed, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_valid_length_name(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the name field should not be more than 100 characters"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        name_value = "a" * 101
        input_page.entity2.name.set_value(name_value)
        self.assert_util(
            input_page.entity2.save,
            r"Length of input name should be between 1 and 100",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_valid_input_name(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies whether adding special characters, name field displays validation error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("$$test_name_two")
        self.assert_util(
            input_page.entity2.save,
            r"Input Name must begin with a letter and consist exclusively of alphanumeric characters and underscores.",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_required_field_interval(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field interval in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("dummy_input")
        input_page.entity2.example_checkbox.check()
        input_page.entity2.example_radio.select("No")
        input_page.entity2.example_multiple_select.select("Option One")
        input_page.entity2.index.select("main")
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity2.save,
            r"Field Interval is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_valid_input_interval(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies whether adding non numeric values, intreval field displays validation error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("test_name_two")
        input_page.entity2.interval.set_value("abc")
        self.assert_util(
            input_page.entity2.save,
            r"Interval must be either a non-negative number or -1.",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_required_field_index(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field index in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("dummy_input")
        input_page.entity2.example_checkbox.check()
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.example_radio.select("No")
        input_page.entity2.example_multiple_select.select("Option One")
        input_page.entity2.interval.set_value("90")
        input_page.entity2.query_start_date.set_value("2020-12-11T20:00:32.000z")
        input_page.entity2.index.cancel_selected_value()
        self.assert_util(
            input_page.entity2.save,
            r"Field Index is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_default_value_index(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default value of field index in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        default_index = "default"
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(input_page.entity2.index.get_value, default_index)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_required_field_example_example_account(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field Account in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("dummy_input")
        input_page.entity2.example_checkbox.check()
        input_page.entity2.example_radio.select("No")
        input_page.entity2.example_multiple_select.select("Option One")
        input_page.entity2.index.select("main")
        input_page.entity2.interval.set_value("90")
        input_page.entity2.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity2.save,
            r"Field Example Account is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_required_field_example_multiple_select(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies required field Example Multiple Select in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("dummy_input")
        input_page.entity2.example_checkbox.check()
        input_page.entity2.example_radio.select("No")
        input_page.entity2.index.select("main")
        input_page.entity2.interval.set_value("90")
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity2.save,
            r"Field Example Multiple Select is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_list_example_multiple_select(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies values of Multiple Select Test dropdown in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        example_multiple_select_list = ["Option One", "Option Two"]
        self.assert_util(
            input_page.entity2.example_multiple_select.list_of_values(),
            example_multiple_select_list,
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_select_select_value_example_multiple_select(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies selected single value of Multiple Select Test dropdown in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        selected_value = ["Option One"]
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.index.select("main")
        for each in selected_value:
            input_page.entity2.example_multiple_select.select(each)
        self.assert_util(
            input_page.entity2.example_multiple_select.get_values, selected_value
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_select_multiple_values_example_multiple_select(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies selected multiple values of Multiple Select Test dropdown in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        selected_values = ["Option One", "Option Two"]
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.index.select("main")
        for each in selected_values:
            input_page.entity2.example_multiple_select.select(each)
        self.assert_util(
            input_page.entity2.example_multiple_select.get_values, selected_values
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_help_text_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies help text for the field name"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(
            input_page.entity2.example_multiple_select.get_help_text,
            "This is an example multipleSelect for input two entity",
        )
        self.assert_util(
            input_page.entity2.name.get_help_text, "A unique name for the data input."
        )
        self.assert_util(
            input_page.entity2.interval.get_help_text,
            "Time interval of the data input, in seconds .",
        )
        self.assert_util(
            input_page.entity2.example_checkbox.get_help_text,
            "This is an example checkbox for the input two entity",
        )
        self.assert_util(
            input_page.entity2.example_radio.get_help_text,
            "This is an example radio button for the input two entity",
        )
        self.assert_util(
            input_page.entity2.query_start_date.get_help_text,
            'The date and time, in "YYYY-MM-DDThh:mm:ss.000z" format, after which to query and index records. The default is 90 days before today.',
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_checked_example_checkbox(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies Check in example checkbox in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(input_page.entity2.example_checkbox.check, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_unchecked_example_checkbox(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies Uncheck in example checkbox in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.example_checkbox.check()
        self.assert_util(input_page.entity2.example_checkbox.uncheck, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_required_field_example_radio(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default value of example radio in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("dummy_input")
        input_page.entity2.example_checkbox.check()
        input_page.entity2.example_multiple_select.select("Option One")
        input_page.entity2.index.select("main")
        input_page.entity2.interval.set_value("90")
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(
            input_page.entity2.save,
            r"Field Example Radio is required",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_select_value_example_radio(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies default value of example radio in Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.example_radio.select("No")
        self.assert_util(input_page.entity2.example_radio.get_value, "No")

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_valid_input_query_start_date(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies whether adding wrong format, Query Start Date field displays validation error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("test_name_two")
        input_page.entity2.interval.set_value("120")
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.example_multiple_select.select("Option One")
        input_page.entity2.example_radio.select("Yes")
        input_page.entity2.query_start_date.set_value("2020/01/01")
        self.assert_util(
            input_page.entity2.save,
            r"Invalid date and time format",
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_two_add_frontend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the frontend after adding a Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("dummy_input")
        input_page.entity2.example_checkbox.check()
        input_page.entity2.example_radio.select("No")
        input_page.entity2.example_multiple_select.select("Option One")
        input_page.entity2.example_multiple_select.select("Option Two")
        input_page.entity2.index.select("main")
        input_page.entity2.interval.set_value("90")
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(input_page.entity2.save, True)
        input_page.table.wait_for_rows_to_appear(1)
        self.assert_util(
            input_page.table.get_table()["dummy_input"],
            {
                "name": "dummy_input",
                "account": "test_input",
                "interval": "90",
                "index": "main",
                "status": "Enabled",
                "actions": "Edit | Clone | Delete",
            },
        )
        url = input_page._get_input_endpoint()

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_two_add_backend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the backend after adding a Example Input Two"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("dummy_input")
        input_page.entity2.example_checkbox.check()
        input_page.entity2.example_radio.select("No")
        input_page.entity2.example_multiple_select.select("Option One")
        input_page.entity2.example_multiple_select.select("Option Two")
        input_page.entity2.index.select("main")
        input_page.entity2.interval.set_value("90")
        input_page.entity2.checkboxgroup.select_checkbox_and_set_value(
            "EC2", "ec2_instances", "100"
        )
        input_page.entity2.checkboxgroup.select_checkbox_and_set_value(
            "ELB", "classic_load_balancers", "100"
        )
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.query_start_date.set_value("2020-12-11T20:00:32.000z")
        self.assert_util(input_page.entity2.save, True)
        input_page.table.wait_for_rows_to_appear(1)
        value_to_test = {
            "account": "test_input",
            "index": "main",
            "input_two_checkbox": "1",
            "input_two_radio": "0",
            "interval": "90",
            "input_two_multiple_select": "one,two",
            "start_date": "2020-12-11T20:00:32.000z",
            "disabled": 0,
            "apis": "ec2_volumes/3600,ec2_instances/100,classic_load_balancers/100",
        }
        backend_stanza = input_page.backend_conf.get_stanza(
            "example_input_two://dummy_input"
        )
        for each_key, each_value in value_to_test.items():
            self.assert_util(each_value, backend_stanza[each_key])

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_edit_uneditable_field_name(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the frontend uneditable fields at time of edit of the Example Input Two entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(input_page.entity2.name.is_editable, False)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_two_edit_frontend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the frontend edit functionality of the Example Input Two entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.example_checkbox.uncheck()
        input_page.entity2.example_radio.select("Yes")
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.example_multiple_select.deselect("Option One")
        input_page.entity2.interval.set_value("3600")
        input_page.entity2.query_start_date.set_value("2020-20-20T20:20:20.000z")
        self.assert_util(input_page.entity2.save, True)
        input_page.table.wait_for_rows_to_appear(1)
        self.assert_util(
            input_page.table.get_table()["dummy_input_two"],
            {
                "name": "dummy_input_two",
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
    def test_example_input_two_edit_backend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the backend edit functionality of the Example Input Two entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.example_checkbox.uncheck()
        input_page.entity2.example_account.select("test_input")
        input_page.entity2.example_radio.select("Yes")
        input_page.entity2.example_multiple_select.deselect("Option One")
        input_page.entity2.interval.set_value("3600")
        input_page.entity2.query_start_date.set_value("2020-20-20T20:20:20.000z")
        input_page.entity2.checkboxgroup.deselect("EC2", "ec2_instances")
        input_page.entity2.checkboxgroup.deselect("ELB", "classic_load_balancers")
        self.assert_util(
            input_page.entity2.checkboxgroup.get_textbox(
                "classic_load_balancers"
            ).is_editable(),
            False,
        )
        input_page.entity2.checkboxgroup.select_checkbox_and_set_value(
            "VPC", "vpcs", "1000"
        )
        self.assert_util(input_page.entity2.save, True)
        input_page.table.wait_for_rows_to_appear(1)
        value_to_test = {
            "account": "test_input",
            "input_two_checkbox": "0",
            "input_two_radio": "1",
            "interval": "3600",
            "index": "main",
            "input_two_multiple_select": "two",
            "start_date": "2020-20-20T20:20:20.000z",
            "disabled": 0,
            "apis": "ec2_volumes/3600,vpcs/1000",
        }
        backend_stanza = input_page.backend_conf.get_stanza(
            "example_input_two://dummy_input_two"
        )
        for each_key, each_value in value_to_test.items():
            self.assert_util(each_value, backend_stanza[each_key])

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_clone_default_values(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the frontend default fields at time of clone for Example Input Two entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(input_page.entity2.name.get_value, "")
        self.assert_util(input_page.entity2.example_checkbox.is_checked, True)
        self.assert_util(input_page.entity2.example_radio.get_value, "No")
        self.assert_util(
            input_page.entity2.example_multiple_select.get_values,
            ["Option One", "Option Two"],
        )
        self.assert_util(input_page.entity2.interval.get_value, "100")
        self.assert_util(input_page.entity2.index.get_value, "main")
        self.assert_util(input_page.entity2.example_account.get_value, "test_input")
        self.assert_util(
            input_page.entity2.query_start_date.get_value, "2016-10-10T12:10:15.000z"
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_two_clone_frontend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the frontend clone functionality of the Example Input Two entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.wait_for_rows_to_appear(1)
        input_page.table.clone_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("dummy_input_two_Clone_Test")
        input_page.entity2.interval.set_value("180")
        self.assert_util(input_page.entity2.save, True)
        input_page.table.wait_for_rows_to_appear(2)
        self.assert_util(
            input_page.table.get_table()["dummy_input_two_Clone_Test"],
            {
                "name": "dummy_input_two_Clone_Test",
                "account": "test_input",
                "interval": "180",
                "index": "main",
                "status": "Enabled",
                "actions": "Edit | Clone | Delete",
            },
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_two_clone_backend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the backend clone functionality of the Example Input Two entity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.wait_for_rows_to_appear(1)
        input_page.table.clone_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.name.set_value("Clone_Test")
        input_page.entity2.interval.set_value("180")
        self.assert_util(input_page.entity2.save, True)
        input_page.table.wait_for_rows_to_appear(2)
        value_to_test = {
            "account": "test_input",
            "input_two_checkbox": "1",
            "input_two_radio": "0",
            "interval": "180",
            "index": "main",
            "input_two_multiple_select": "one,two",
            "start_date": "2016-10-10T12:10:15.000z",
            "disabled": 0,
        }
        backend_stanza = input_page.backend_conf.get_stanza(
            "example_input_two://Clone_Test"
        )
        for each_key, each_value in value_to_test.items():
            self.assert_util(each_value, backend_stanza[each_key])

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_two_delete_row_frontend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the frontend delete functionlity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.input_status_toggle("dummy_input_two", enable=False)
        input_page.table.delete_row("dummy_input_two")
        input_page.table.wait_for_rows_to_appear(0)
        self.assert_util("dummy_input_two", input_page.table.get_table, "not in")

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    @pytest.mark.sanity_test
    def test_example_input_two_delete_row_backend_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the backend delete functionlity"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.input_status_toggle("dummy_input_two", enable=False)
        input_page.table.delete_row("dummy_input_two")
        input_page.table.wait_for_rows_to_appear(0)
        self.assert_util(
            "example_input_two://dummy_input_two",
            input_page.backend_conf.get_all_stanzas().keys(),
            "not in",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_add_close_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies close functionality at time of add"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(input_page.entity2.close, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_edit_close_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies close functionality at time of edit"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_two")
        self.assert_util(input_page.entity2.close, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_clone_close_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies close functionality at time of clone"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_two")
        self.assert_util(input_page.entity2.close, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_delete_close_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies close functionality at time of delete"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(
            input_page.table.delete_row,
            True,
            left_args={"name": "dummy_input_two", "close": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_add_cancel_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies cancel functionality at time of add"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(input_page.entity2.cancel, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_edit_cancel_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies cancel functionality at time of edit"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_two")
        self.assert_util(input_page.entity2.cancel, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_clone_cancel_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies cancel functionality at time of clone"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_two")
        self.assert_util(input_page.entity2.cancel, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_delete_cancel_entity(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies cancel functionality at time of delete"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(
            input_page.table.delete_row,
            True,
            left_args={"name": "dummy_input_two", "cancel": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_add_duplicate_names(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies by saving an entity with duplicate name it displays and error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_name = "dummy_input_two"
        input_page.entity2.name.set_value(input_name)
        self.assert_util(
            input_page.entity2.save,
            "Name {} is already in use".format(input_name),
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_clone_duplicate_names(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies by saving an entity with duplicate name at time of clone it displays and error"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        input_name = "dummy_input_two"
        input_page.entity2.name.set_value(input_name)
        self.assert_util(
            input_page.entity2.save,
            "Name {} is already in use".format(input_name),
            left_args={"expect_error": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_add_valid_title(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the title of the 'Add Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(
            input_page.entity2.title.container.get_attribute("textContent").strip(),
            "Add Example Input Two",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_edit_valid_title(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the title of the 'Edit Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.edit_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(
            input_page.entity2.title.container.get_attribute("textContent").strip(),
            "Update Example Input Two",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_clone_valid_title(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the title of the 'Clone Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.clone_row("dummy_input_two")
        input_page.entity2.example_account.wait_for_values()
        self.assert_util(
            input_page.entity2.title.container.get_attribute("textContent").strip(),
            "Clone Example Input Two",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_delete_valid_title(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the title of the 'Delete Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.delete_row("dummy_input_two", prompt_msg=True)
        self.assert_util(
            input_page.entity2.title.container.get_attribute("textContent").strip(),
            "Delete Confirmation",
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_delete_valid_prompt_message(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_two
    ):
        """Verifies the prompt message of the 'Delete Entity'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_name = "dummy_input_two"
        prompt_message = input_page.table.delete_row("dummy_input_two", prompt_msg=True)
        self.assert_util(
            prompt_message, 'Are you sure you want to delete "{}" ?'.format(input_name)
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_example_input_two_checkboxgroup_validation(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the checkboxgroup component'"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.create_new_input.select("Example Input Two")
        input_page.entity2.example_account.wait_for_values()
        input_page.entity2.checkboxgroup.select_checkbox_and_set_value(
            "EC2", "ec2_instances", "100"
        )
        input_page.entity2.checkboxgroup.collapse_group("EC2")
        self.assert_util(
            input_page.entity2.checkboxgroup.is_group_expanded("EC2"), False
        )
        self.assert_util(
            input_page.entity2.checkboxgroup.get_checkbox_text_value(
                "EC2", "ec2_instances"
            ),
            "100",
        )
