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
from PyQt4.QtGui import QHBoxLayout, QComboBox, QIcon, QLabel, QLineEdit
import PyQt4.QtCore
import os
import pyherc

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

        self.player_character = None

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.setSizePolicy(QSizePolicy(
                                       QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))

        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton('Ok', self)
        self.ok_button.resize(self.ok_button.sizeHint())
        self.ok_button.clicked.connect(self.__generate_character)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.resize(self.cancel_button.sizeHint())
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.name_layout = QHBoxLayout()
        self.name_label = QLabel('Name:', self)
        self.name_text = QLineEdit('Adventurer', self)
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_text)

        self.kit_selection_layout = QHBoxLayout()
        self.kit_selection_label = QLabel('Kit:', self)
        self.kit_selection = QComboBox(self)
        self.kit_selection.addItem('Adventurer')
        self.kit_selection.addItem('Vampire Hunter')
        self.kit_selection_layout.addWidget(self.kit_selection_label)
        self.kit_selection_layout.addWidget(self.kit_selection)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addLayout(self.name_layout)
        self.vertical_layout.addLayout(self.kit_selection_layout)
        self.vertical_layout.addLayout(self.button_layout)

        self.setLayout(self.vertical_layout)

        self.ok_button.setDefault(True)

        self.setWindowTitle('New game')
        self.setWindowIcon(QIcon(os.path.join(self.application.base_path,
                                                'cycle.png')))

    def __generate_character(self):
        """
        Generate player character based on selected settings
        """
        self.player_character = pyherc.rules.character.create_character('human',
                                                'fighter',
                                                self.application.world)
        self.player_character.name = self.name_text.displayText()
        self.accept()
