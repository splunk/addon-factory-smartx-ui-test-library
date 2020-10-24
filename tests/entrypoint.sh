#!/bin/sh
##
## SPDX-FileCopyrightText: 2020 Splunk, Inc. <sales@splunk.com>
## SPDX-License-Identifier: LicenseRef-Splunk-1-2020
##
##

cd /home/circleci/work
echo Test Args pytest $@ ${TEST_SUITE} --browser=${TEST_BROWSER}
pytest $@ ${TEST_SUITE} --browser=${TEST_BROWSER}