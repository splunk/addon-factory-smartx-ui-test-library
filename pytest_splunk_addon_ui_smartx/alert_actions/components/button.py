# SPDX-FileCopyrightText: 2020 2020
#
# SPDX-License-Identifier: Apache-2.0

from ...components.controls.button import Button
from .action_controls import ActionControls

class Button(Button, ActionControls):
    def __init__(self, browser, container):
        super(Button, self).__init__(browser, container)