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
from PyQt4.QtCore import Qt
import PyQt4.QtCore
import os
import pyherc

class StartGameWidget(QDialog):
    """
    Start menu

    .. versionadded:: 0.5
    """

    def __init__(self, config, parent, application, surface_manager, flags):
        """
        Default constructor
        """
        super(StartGameWidget, self).__init__(parent, flags)

        self.application = application
        self.surface_manager = surface_manager

        if config != None:
            self.config = config
        else:
            self.config = []

        self.player_character = None

        self.__set_layout()

    def __set_layout(self):
        """
        Set layout of this widget
        """
        self.setSizePolicy(QSizePolicy(
                                       QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))

        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        middle_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)

        self.class_name = QLabel('')
        self.class_name.setMinimumSize(200, 50)
        self.class_name.setMaximumSize(200, 50)
        self.class_name.setAlignment(Qt.AlignCenter);
        self.class_icon = QLabel('')
        self.class_icon.setMinimumSize(100, 100)
        self.class_icon.setMaximumSize(100, 100)
        self.class_description = QLabel('')
        self.class_description.setWordWrap(True)
        self.class_description.setMinimumSize(600, 300)
        self.class_description.setMaximumSize(600, 300)
        self.class_description.setAlignment(Qt.AlignTop);

        top_layout.addStretch()
        top_layout.addWidget(self.class_name)
        top_layout.addStretch()
        middle_layout.addStretch()
        middle_layout.addWidget(self.class_icon)
        middle_layout.addStretch()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.class_description)
        bottom_layout.addStretch()

        self.setLayout(main_layout)

        self.setWindowTitle('New game')
        #self.setWindowIcon(QIcon(os.path.join(self.application.base_path,
        #                                        'cycle.png')))

        if len(self.config) > 0:
            self._show_character(self.config[0])

    def _show_character(self, character):
        """
        Show character on screen

        .. versionadded:: 0.8
        """
        self.class_name.setText(character.class_name)
        self.class_description.setText(character.class_description)

    def __generate_character(self):
        """
        Generate player character based on selected settings
        """
        self.player_character = None
        self.player_character = pyherc.rules.character.create_character('human',
                                                'fighter',
                                                self.application.world)
        self.accept()
