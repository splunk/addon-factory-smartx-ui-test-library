#
# Copyright 2021 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json


def get_orca_deployment_urls():
    """
    Fetch the web_url and management_url from the orca_deployment.json file to execute the testcases.
    reason: In windows containers "so1" hostname does not work directly.
    """
    try:
        with open("orca_deployment.json") as f:
            data = f.read()
        json_data = json.loads(data)

    except Exception as e:
        print(str(e))

    web_url = json_data["server_roles"]["standalone"][0]["splunk"]["web_url"]
    mgmt_url = json_data["server_roles"]["standalone"][0]["splunk"]["management_url"]
    return {"web": web_url, "mgmt": mgmt_url}


# Decorator with argument
def backend_retry(retry_count):
    # The decorator itself
    def backend_retry_decorator(method):
        # Inner method in the decorator
        def retry_method(*args, **kwargs):
            last_exc = Exception()

            # Try 3 times
            for _ in range(retry_count):
                try:
                    return method(*args, **kwargs)
                except Exception as e:
                    last_exc = e
            else:
                if last_exc:
                    raise (last_exc)

        return retry_method

    return backend_retry_decorator
