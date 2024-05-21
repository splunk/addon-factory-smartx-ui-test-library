**Creating tests**

These files contain the test suites for the webpages that we want to test. A test generally consists of creating an instance of the webpage class we created above and calling on component functions to manipulate and assert the status of an element on the webpage. The test cases also calls the two SmartX fixtures that creates the Selenium Driver classes that we need for our tests. It is also recommended to add docstrings to each test so that it can be easily identifiable of what each test is trying to accomplish.
The test cases utilize a class function assert_util to conveniently test a plethora of different assertions in a unified way. It is recommended to use this function to keep the code simple and readable. This function has the following parameters:

 - left: The parameter you want to compare/assert with, generally this would be the status of the webelement. This parameter is required.
 - right: The parameter you want to compare/assert with to the left parameter. Generally this would be the state that you want the webelement to be in. This parameter is required.
 - operator: This will be the operator in which you want the left to be compared with the right. The options are as follows: \["==", "!=", "\<", "\<=", ">", ">=", "in", "not in", "is", "is not"\]. This parameter's default: "=="
 - left_args: If the left parameter is a function, then you can provide that function with the arguments found here. This parameter's default: {}
 - right_args: If the right parameter is a function, then you can provide that function with the arguments found here. This parameter's default: {}
 - msg: If you want a custom error message to appear if this assertion fails, then you can add that here, otherwise the default message is as follows: 
 ```
 Condition Failed. 
 Left-value: {} Operator: {} 
 Right-value: {}".format(args['left_value'], args['operator'], args['right_value']).
 ```

For the test cases, you may also want to include informative markers as well so that selectively testing the Addon's UI tests could be easy. Some of the common UI markers we used were:

 - &lt;test_suite&gt;: Test Page UI test cases (i.e. input)
 - forwarder: Tests to be run on Forwarder/Standalone
 - liveenvironment: Tests need live server to successfully execute
 - oauth_account: Oauth Account UI test cases
 - sanity_test: For sanity check of addons

```python
import pytest

from pytest_splunk_addon_ui_smartx.base_test import UccTester
from pytest_splunk_addon_ui_smartx.pages.proxy import Proxy

TA_NAME = "Splunk_TA_<TA_NAME>"
TA_PROXY_URL = (
    "/servicesNS/nobody/Splunk_TA_<TA_NAME>/Splunk_TA_<TA_NAME>_settings/proxy"
)

class TestProxy(UccTester):
    """
    Test suite testing UCC from based configuration page
    """

    @pytest.mark.proxy
    @pytest.mark.forwarder
    def test_proxy_default_configs(
        self, ucc_smartx_selenium_helper, ucc_smartx_rest_helper
    ):
        """
        Verifies the default proxy configurations
        """
        proxy = Proxy(
            TA_NAME,
            TA_PROXY_URL,
            ucc_smartx_selenium_helper=ucc_smartx_selenium_helper,
            ucc_smartx_rest_helper=ucc_smartx_rest_helper,
        )
        self.assert_util(proxy.proxy_enable.is_checked(), False)
        self.assert_util(proxy.dns_enable.is_checked(), False)
        self.assert_util(proxy.type.get_value(), "http")
        self.assert_util(proxy.host.get_value(), "")
        self.assert_util(proxy.port.get_value(), "")
        self.assert_util(proxy.username.get_value(), "")
        self.assert_util(proxy.password.get_value(), "")

```


**Setup Fixtures**

The test suite could also contain setup fixtures that would be called before tests to setup the Splunk environment. This could range from creating new inputs, to using a different page class to create a related input/Account for the page being tested. It may also be useful to have global variables for the default configurations so that it could be easily edited and reused later.
An example of a setup fixture:

```python
ACCOUNT_PARAMS = {
    "name": "test_account",
    "endpoint": "login.test.com",
    "username": None,
    "password": None,
}


@pytest.fixture(scope="class", autouse=True)
def create_account(ucc_smartx_rest_helper):
    """
    Fixture to create account using rest endpoint
    """
    account = AccountPage(
        ucc_smartx_rest_helper=ucc_smartx_rest_helper, open_page=False
    )
    url = account._get_account_endpoint()
    account_config = {
        "name": ACCOUNT_PARAMS.get("name"),
        "endpoint": ACCOUNT_PARAMS.get("endpoint"),
        "username": ACCOUNT_PARAMS.get("username"),
        "password": ACCOUNT_PARAMS.get("password"),
    }
    account.backend_conf.post_stanza(url, account_config)
    yield
    account.backend_conf.delete_all_stanzas()

```


**Teardown Fixtures**

The test suites should also contain teardown fixtures to revert the Splunk instance back to its original state after each test, this way each test is independent of each other and so if one test fails, then another test shouldn't fail in correspondence as to the first test.
An example of the teardown fixture:

```python
DEFAULT_CONFIGURATION = {
    "proxy_enabled": "",
    "proxy_password": "",
    "proxy_port": "",
    "proxy_rdns": "",
    "proxy_type": "http",
    "proxy_url": "",
    "proxy_username": "",
}


@pytest.fixture(autouse=True)
def reset_configuration(ucc_smartx_rest_helper):
    yield
    proxy = Proxy(TA_NAME, TA_PROXY_URL, ucc_smartx_rest_helper=ucc_smartx_rest_helper)
    proxy.backend_conf_post.update_parameters(DEFAULT_CONFIGURATION)

```


**Environment Variables**

You may also want to get environment variables so that you can dynamically setup different test variables easily through the environment instead of having to hardcode them into the test. This may useful in hiding sensitive data such as login credentials.
An example for getting environment variables is as follows:

```python
@pytest.fixture(scope="session", autouse=True)
def get_account_credentials():
    """
    Fixtures to fetch credentials from environment variables
    """
    ACCOUNT_PARAMS["username"] = b64decode(os.getenv("USERNAME")).decode("ascii")
    ACCOUNT_PARAMS["password"] = b64decode(os.getenv("PASSWORD")).decode("ascii")
    ACCOUNT_PARAMS["token"] = b64decode(os.getenv("TOKEN")).decode("ascii")

```
