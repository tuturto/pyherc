#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2012 Tuukka Turto
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
from PyQt4.QtGui import QDialog, QVBoxLayout
from PyQt4.QtCore import Qt

class EndScreen(QDialog):
    """
    Dialog to show end screen

    .. versionadded:: 0.8
    """
    def __init__(self, model, config, parent, flags):
        """
        Default constructor
        """
        super(EndScreen, self).__init__(parent, flags)

        self.__set_layout(model,
                          config,
                          parent)

    def __set_layout(self, model, config, parent):
        """
        Set layout of this widget
        """
        self.keymap = self._construct_keymap(config)

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
