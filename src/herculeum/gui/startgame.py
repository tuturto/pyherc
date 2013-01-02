#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2010-2013 Tuukka Turto
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

from PyQt4.QtGui import QDialog, QSizePolicy, QVBoxLayout
from PyQt4.QtGui import QHBoxLayout, QLabel
from PyQt4.QtCore import Qt
import PyQt4.QtCore

class StartGameWidget(QDialog):
    """
    Start menu

    .. versionadded:: 0.5
    """

    def __init__(self, generator, config,
                 parent, application, surface_manager, flags):
        """
        Default constructor
        """
        super(StartGameWidget, self).__init__(parent, flags)

        self.application = application
        self.surface_manager = surface_manager
        self.config = config

        self.generator = generator

        self.player_character = None
        self.class_description = None
        self.class_name = None
        self.class_icon = None
        self.selected_index = None
        self.class_names = None

        cnf = self.config
        self.konami = [cnf.move_up, cnf.move_up,
                       cnf.move_down, cnf.move_down,
                       cnf.move_left, cnf.move_right,
                       cnf.move_left, cnf.move_right,
                       cnf.action_b, cnf.action_a]
        self.konami_index = 0

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

        self.class_names = self.generator.configuration.keys()
        self.class_names.sort()

        self.selected_index = 0
        if len(self.class_names) > 0:
            self._show_character(
                    self.generator.configuration[self.class_names[self.selected_index]])

    def _show_character(self, character):
        """
        Show character on screen

        .. versionadded:: 0.8
        """
        self.class_name.setText(character.name)
        self.class_description.setText(character.description)

    def __generate_character(self):
        """
        Generate player character based on selected settings
        """
        self.player_character = None
        self.player_character = self.generator.generate_creature(
                                            name = self.class_names[self.selected_index])

    def keyPressEvent(self, event):
        """
        Process keyboard events
        """
        if event.key() in self.konami[self.konami_index]:
            self.konami_index = self.konami_index + 1
        else:
            self.konami_index = 0

        if self.konami_index == len(self.konami):
            self.application.enable_cheat()

        if event.key() in self.config.action_a:
            self.__generate_character()
            self.accept()
        elif event.key() in self.config.move_right:
            self.selected_index = self.selected_index + 1
            if self.selected_index >= len(self.class_names):
                self.selected_index = 0
            self._show_character(
                    self.generator.configuration[self.class_names[self.selected_index]])
        elif event.key() in self.config.move_left:
            self.selected_index = self.selected_index - 1
            if self.selected_index < 0:
                self.selected_index = len(self.class_names) - 1
            self._show_character(
                    self.generator.configuration[self.class_names[self.selected_index]])
        else:
            super(StartGameWidget, self).keyPressEvent(event)
