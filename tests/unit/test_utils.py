from unittest.mock import mock_open, patch

from pytest_splunk_addon_ui_smartx.utils import get_orca_deployment_urls

ORCA_DEPLOYMENT_JSON = """{
    "deployment_type": "custom_cluster",
    "infra_type": "ucp",
    "orca_deployment_id": "srv_releases2102151456184br2m",
    "orca_user": "srv_releases",
    "server_roles": {
        "custom": [
            {
                "orca_service": "sc4s0",
                "ports": {
                    "514/tcp": "10.141.67.102:31119"
                },
                "private_address": "10.157.3.3"
            }
        ],
        "standalone": [
            {
                "host": "10.141.66.22",
                "ports": {
                    "1514/tcp": "10.141.66.22:30232",
                    "2222/tcp": "10.141.66.22:30231",
                    "3333/tcp": "10.141.66.22:30230",
                    "3333/udp": "10.141.66.22:35333",
                    "4001/tcp": "10.141.66.22:30229",
                    "8000/tcp": "10.141.66.22:30228",
                    "8065/tcp": "Unmapped",
                    "8088/tcp": "10.141.66.22:30227",
                    "8089/tcp": "10.141.66.22:30226",
                    "8091/tcp": "10.141.66.22:30225",
                    "8191/tcp": "10.141.66.22:30224",
                    "9021/tcp": "10.141.66.22:30223",
                    "9887/tcp": "Unmapped",
                    "9997/tcp": "10.141.66.22:30222"
                },
                "private_address": "10.157.3.7",
                "splunk": {
                    "build": "8ed5320d8a57",
                    "home": "/opt/splunk",
                    "management_url": "https://10.141.66.22:30226",
                    "product": "splunk",
                    "user_roles": {
                        "admin": {
                            "password": "Chang3d!",
                            "username": "admin"
                        }
                    },
                    "version": "8.0.2006",
                    "web_url": "http://10.141.66.22:30228"
                },
                "ssh": {
                    "key": "/root/.ssh/id_rsa",
                    "port": 30231,
                    "username": "splunk"
                }
            }
        ],
        "testrunner": [
            {
                "host": "10.141.65.21",
                "ports": {
                    "1514/tcp": "10.141.65.21:25769",
                    "22/tcp": "Unmapped",
                    "2222/tcp": "10.141.65.21:25768",
                    "3333/tcp": "10.141.65.21:25767",
                    "3333/udp": "10.141.65.21:34933",
                    "4001/tcp": "10.141.65.21:25766",
                    "5900/tcp": "10.141.65.21:25765",
                    "8000/tcp": "10.141.65.21:25764",
                    "8088/tcp": "10.141.65.21:25763",
                    "8089/tcp": "10.141.65.21:25762",
                    "8091/tcp": "10.141.65.21:25761",
                    "8191/tcp": "10.141.65.21:25760",
                    "9021/tcp": "10.141.65.21:25759",
                    "9997/tcp": "10.141.65.21:25758"
                },
                "private_address": "10.157.3.5"
            }
        ]
    },
    "version": "2.0"
}"""


def test_global_parameters():
    expected = {
        "web": "http://10.141.66.22:30228",
        "mgmt": "https://10.141.66.22:30226",
    }
    with patch("builtins.open", mock_open(read_data=ORCA_DEPLOYMENT_JSON)) as json_mock:
        assert get_orca_deployment_urls() == expected
        json_mock.assert_called_with("orca_deployment.json")
