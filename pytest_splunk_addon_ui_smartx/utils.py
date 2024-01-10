#
# Copyright 2024 Splunk Inc.
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
                    raise last_exc

        return retry_method

    return backend_retry_decorator
