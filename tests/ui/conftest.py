import pytest

from tests.ui.Example_UccLib.account import AccountPage


@pytest.fixture
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
