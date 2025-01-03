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

from typing import List, NamedTuple, Optional
from enum import Enum, auto


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


class LogLevel(Enum):
    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    SEVERE = auto()


class LogSource(Enum):
    NETWORK = "network"
    CONSOLE_API = "console-api"
    RECOMMENDATION = "recommendation"
    SECURITY = "security"
    INTERVENTION = "intervention"
    JAVASCRIPT = "javascript"


class LogEntry(NamedTuple):
    level: LogLevel
    message: str
    source: LogSource
    timestamp: int


def get_browser_logs(
    browser,
    log_level: Optional[LogLevel] = None,
    log_source: Optional[LogSource] = None,
) -> List[LogEntry]:
    """
    Retrieve and optionally filter browser console logs.
    """
    if browser.name.lower() != "chrome":
        return []

    logs = browser.get_log("browser")
    filtered_logs: List[LogEntry] = []

    for log in logs:
        entry = LogEntry(
            level=LogLevel[log["level"]],
            message=log["message"],
            source=LogSource(log["source"]),
            timestamp=log["timestamp"],
        )

        if (log_level is None or entry.level == log_level) and (
            log_source is None or entry.source == log_source
        ):
            filtered_logs.append(entry)

    return filtered_logs
