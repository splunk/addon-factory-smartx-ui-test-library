#
# Copyright 2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from unittest.mock import Mock, patch

import pytest

from pytest_splunk_addon_ui_smartx.backend_confs import ListBackendConf


def response(status_code, text="", json_data=None):
    result = Mock(status_code=status_code, text=text)
    result.json.return_value = json_data
    return result


@pytest.fixture
def backend_conf():
    return ListBackendConf(
        "https://splunk.example/private_account", "admin", "password"
    )


def test_post_stanza_retries_503_after_confirming_stanza_is_absent(backend_conf):
    with (
        patch(
            "pytest_splunk_addon_ui_smartx.backend_confs.requests.post",
            side_effect=[
                response(503, "upstream connect error"),
                response(201, json_data={}),
            ],
        ) as post,
        patch(
            "pytest_splunk_addon_ui_smartx.backend_confs.requests.get",
            return_value=response(404),
        ) as get,
        patch("pytest_splunk_addon_ui_smartx.backend_confs.time.sleep") as sleep,
    ):
        backend_conf.post_stanza(backend_conf.url, {"name": "test_account"})

    assert post.call_count == 2
    get.assert_called_once()
    sleep.assert_called_once_with(0.5)


def test_post_stanza_does_not_retry_when_stanza_exists(backend_conf):
    with (
        patch(
            "pytest_splunk_addon_ui_smartx.backend_confs.requests.post",
            return_value=response(503, "upstream reset before headers"),
        ) as post,
        patch(
            "pytest_splunk_addon_ui_smartx.backend_confs.requests.get",
            return_value=response(200),
        ) as get,
        patch("pytest_splunk_addon_ui_smartx.backend_confs.time.sleep") as sleep,
    ):
        with pytest.raises(AssertionError, match="status_code=503"):
            backend_conf.post_stanza(backend_conf.url, {"name": "test_account"})

    post.assert_called_once()
    get.assert_called_once()
    sleep.assert_not_called()


def test_post_stanza_stops_after_bounded_503_retries(backend_conf):
    with (
        patch(
            "pytest_splunk_addon_ui_smartx.backend_confs.requests.post",
            return_value=response(503, "upstream connect error"),
        ) as post,
        patch(
            "pytest_splunk_addon_ui_smartx.backend_confs.requests.get",
            return_value=response(404),
        ) as get,
        patch("pytest_splunk_addon_ui_smartx.backend_confs.time.sleep") as sleep,
    ):
        with pytest.raises(AssertionError, match="status_code=503"):
            backend_conf.post_stanza(backend_conf.url, {"name": "test_account"})

    assert post.call_count == 3
    assert get.call_count == 2
    assert [call.args[0] for call in sleep.call_args_list] == [0.5, 1.0]


def test_post_stanza_does_not_retry_non_transient_response(backend_conf):
    with (
        patch(
            "pytest_splunk_addon_ui_smartx.backend_confs.requests.post",
            return_value=response(400, "invalid configuration"),
        ) as post,
        patch("pytest_splunk_addon_ui_smartx.backend_confs.requests.get") as get,
        patch("pytest_splunk_addon_ui_smartx.backend_confs.time.sleep") as sleep,
    ):
        with pytest.raises(AssertionError, match="status_code=400"):
            backend_conf.post_stanza(backend_conf.url, {"name": "test_account"})

    post.assert_called_once()
    get.assert_not_called()
    sleep.assert_not_called()
