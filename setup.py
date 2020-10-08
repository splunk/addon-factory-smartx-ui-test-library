#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


setup(
    name="pytest-ucc-smartx",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=[
        "pytest-splunk-addon",
        "pytest-html",
        "selenium",
        "future~=0.17.1",
        "configparser",
        "urllib3~=1.21.1",
        "webdriver_manager"
    ],
    extras_require={"docker": ["lovely-pytest-docker>=0.1.0"]},
    setup_requires=["pytest-runner"],
    packages=find_packages(include=["ucc_smartx", "ucc_smartx.*"]),
    test_suite="tests",
    version="0.0.1",
    entry_points={
        "pytest11": [
            "ucc-smartx = ucc_smartx.plugin",
        ],
    }
)
