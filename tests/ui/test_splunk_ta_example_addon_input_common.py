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
    def test_inputs_displayed_columns(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies headers of input table"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        header_list = ["Name", "Account", "Interval", "Index", "Status", "Actions"]
        self.assert_util(input_page.table.get_headers, header_list)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_pagination_list(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies pagination list"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(
            input_page.pagination.get_pagination_list,
            ["10 Per Page", "25 Per Page", "50 Per Page"],
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_pagination(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_multiple_inputs
    ):
        """Verifies pagination functionality by creating 100 accounts"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.open()
        self.assert_util(
            input_page.pagination.select_page_option,
            True,
            left_args={"value": "50 Per Page"},
        )
        self.assert_util(input_page.table.switch_to_page, True, left_args={"value": 2})
        self.assert_util(input_page.table.switch_to_prev, True)
        self.assert_util(input_page.table.switch_to_next, True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_sort_functionality(
        self,
        ucc_smartx_selenium_helper,
        ucc_smartx_rest_helper,
        add_input_one,
        add_input_two,
    ):
        """Verifies sorting functionality for name column"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.pagination.select_page_option("50 Per Page")
        input_page.table.sort_column("Name")
        sort_order = input_page.table.get_sort_order()
        column_values = list(input_page.table.get_column_values("Name"))
        column_values = list(str(item) for item in column_values)
        sorted_values = sorted(column_values, key=str.lower)
        self.assert_util(sort_order["header"].lower(), "name")
        self.assert_util(column_values, sorted_values)
        self.assert_util(sort_order["ascending"], True)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_filter_functionality_negative(
        self,
        ucc_smartx_selenium_helper,
        ucc_smartx_rest_helper,
        add_input_one,
        add_input_two,
    ):
        """Verifies the filter functionality (Negative)"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.set_filter("hello")
        self.assert_util(input_page.table.get_row_count, 0)
        self.assert_util(
            input_page.table.get_count_title,
            "{} Input".format(input_page.table.get_row_count()),
        )
        input_page.table.clean_filter()

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_filter_functionality_positive(
        self,
        ucc_smartx_selenium_helper,
        ucc_smartx_rest_helper,
        add_input_one,
        add_input_two,
    ):
        """Verifies the filter functionality (Positive)"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        input_page.table.set_filter("dummy")
        self.assert_util(input_page.table.get_row_count, 2)
        self.assert_util(
            input_page.table.get_count_title,
            "{} Inputs".format(input_page.table.get_row_count()),
        )
        input_page.table.clean_filter()

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_default_rows_in_table(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the default number of rows in the table"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(input_page.table.get_row_count, 0)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_create_new_input_list_values(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies input list dropdown"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        create_new_input_list = ["Example Input One", "Example Input Two"]
        self.assert_util(
            input_page.create_new_input.get_inputs_list, create_new_input_list
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_input_type_list_values(
        self,
        ucc_smartx_selenium_helper,
        ucc_smartx_rest_helper,
        add_input_one,
        add_input_two,
    ):
        """Verifies input type filter list"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        type_filter_list = ["All", "Example Input One", "Example Input Two"]
        self.assert_util(input_page.type_filter.get_input_type_list, type_filter_list)
        input_page.type_filter.select_input_type(
            "Example Input One", open_dropdown=False
        )
        self.assert_util(input_page.table.get_row_count, 1)
        input_page.type_filter.select_input_type("Example Input Two")
        self.assert_util(input_page.table.get_row_count, 1)

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_more_info(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the expand functionality of the inputs table"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(
            input_page.table.get_more_info,
            {
                "Name": "dummy_input_one",
                "Interval": "90",
                "Index": "default",
                "Status": "Enabled",
                "Example Account": "test_input",
                "Object": "test_object",
                "Object Fields": "test_field",
                "Order By": "LastModifiedDate",
                "Query Start Date": "2020-12-11T20:00:32.000z",
                "Limit": "1000",
            },
            left_args={"name": "dummy_input_one"},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_enable_disable(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper, add_input_one
    ):
        """Verifies the enable and disable functionality of the input"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(
            input_page.table.input_status_toggle,
            True,
            left_args={"name": "dummy_input_one", "enable": False},
        )
        self.assert_util(
            input_page.table.input_status_toggle,
            True,
            left_args={"name": "dummy_input_one", "enable": True},
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_count(
        self,
        ucc_smartx_selenium_helper,
        ucc_smartx_rest_helper,
        add_input_one,
        add_input_two,
    ):
        """Verifies count on table"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(
            input_page.table.get_count_title,
            "{} Inputs".format(input_page.table.get_row_count()),
        )

    @pytest.mark.execute_enterprise_cloud_true
    @pytest.mark.forwarder
    @pytest.mark.input
    def test_inputs_title_and_description(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """Verifies the title and description of the page"""
        input_page = InputPage(ucc_smartx_selenium_helper, ucc_smartx_rest_helper)
        self.assert_util(input_page.title.wait_to_display, "Inputs")
        self.assert_util(
            input_page.description.wait_to_display, "Manage your data inputs"
        )
