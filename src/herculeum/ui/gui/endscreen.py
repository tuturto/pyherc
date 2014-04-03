#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
#
#   This file is part of pyherc.
#
#   pyherc is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   pyherc is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with pyherc.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for displaying end screen
"""
from datetime import date

from PyQt4.QtGui import QDialog, QLabel, QVBoxLayout


class EndScreen(QDialog):
    """
    Dialog to show end screen

    .. versionadded:: 0.8
    """
    def __init__(self, model, config, dying_rules, parent, flags,
                 controller):
        """
        Default constructor
        """
        super(EndScreen, self).__init__(parent, flags)

        self.name_label = None
        self.keymap = None
        self.result_label = None
        self.instruction_label = None
        self.date_label = None
        self.score_label = None
        self.dying_rules = dying_rules
        self.controller = controller

        self.__set_layout(model,
                          config,
                          parent)

    def __set_layout(self, model, config, parent):
        """
        Set layout of this widget
        """
        self.keymap = self._construct_keymap(config)

        layout = QVBoxLayout()
        self.name_label = QLabel('Name:' + model.player.name)
        self.name_label.setObjectName('no_border')
        self.date_label = QLabel('Date: ' + str(date.today()))
        self.date_label.setObjectName('no_border')
        self.score_label = QLabel('Score: ' + str(self.dying_rules.calculate_score(model.player)))
        self.score_label.setObjectName('no_border')
        self.result_label = QLabel(self.controller.get_end_description(model.end_condition))
        self.result_label.setObjectName('no_border')
        self.instruction_label = QLabel('Press action A to continue')
        self.instruction_label.setObjectName('no_border')

        layout.addWidget(self.name_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.score_label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.instruction_label)

        self.setLayout(layout)

    def _construct_keymap(self, config):
        """
        Construct key map

        .. versionadded:: 0.8
        """
        keymap = {}

        for key in config.action_a:
            keymap[key] = self._close_window

        return keymap

    def _close_window(self):
        """
        Close the window
        """
        self.done(0)

    def keyPressEvent(self, event):
        """
        Handle keyboard events
        """
        key = event.key()

        if key in self.keymap:
            self.keymap[key]()
        else:
            super(EndScreen, self).keyPressEvent(event)
