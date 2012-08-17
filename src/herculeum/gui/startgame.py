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
Module for start game window related functionality
"""

from PyQt4.QtGui import QDialog, QPushButton, QSizePolicy, QVBoxLayout
from PyQt4.QtGui import QHBoxLayout, QComboBox, QIcon
import PyQt4.QtCore
import os

class StartGameWidget(QDialog):
    """
    Start menu

    .. versionadded:: 0.5
    """

    def __init__(self,  parent, application, surface_manager):
        """
        Default constructor
        """
        super(StartGameWidget, self).__init__(parent)

        self.application = application
        self.surface_manager = surface_manager

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.setSizePolicy(QSizePolicy(
                                       QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))

        horizontal_layout = QHBoxLayout()

        ok_button = QPushButton('Ok', self)
        ok_button.resize(ok_button.sizeHint())

        cancel_button = QPushButton('Cancel', self)
        cancel_button.resize(cancel_button.sizeHint())

        horizontal_layout.addWidget(ok_button)
        horizontal_layout.addWidget(cancel_button)

        vertical_layout = QVBoxLayout()

        kit_selection = QComboBox(self)
        kit_selection.addItem('Adventurer')
        kit_selection.addItem('Vampire Hunter')

        vertical_layout.addWidget(kit_selection)
        vertical_layout.addLayout(horizontal_layout)

        self.setLayout(vertical_layout)

        self.setWindowTitle('New game')
        self.setWindowIcon(QIcon(os.path.join(self.application.base_path,
                                                'cycle.png')))
