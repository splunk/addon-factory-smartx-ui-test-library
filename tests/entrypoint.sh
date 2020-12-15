#!/bin/sh
##
## SPDX-FileCopyrightText: 2020 Splunk, Inc. <sales@splunk.com>
## SPDX-License-Identifier: LicenseRef-Splunk-1-2020
##
##

cd /home/circleci/work
RERUN_COUNT=${RERUN_COUNT:-1}

# Wait for SauceConnect
wget --retry-connrefused --no-check-certificate -T 10 sauceconnect:4445

# Execute tests
echo Test Args = pytest $@ ${TEST_SET} ${TEST_SUITE} --browser=${TEST_BROWSER} --reruns=${RERUN_COUNT}
pytest $@ ${TEST_SET} ${TEST_SUITE} --browser=${TEST_BROWSER} --reruns=${RERUN_COUNT}

# Exit with result
test_exit_code=$?
exit "$test_exit_code" 