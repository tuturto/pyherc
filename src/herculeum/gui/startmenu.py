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
Module for start menu related functionality
"""

import logging
import herculeum.gui.images
import pyherc
import os

from PyQt4.QtGui import QWidget, QPushButton, QSizePolicy
import PyQt4.QtCore

class StartMenuWidget(QWidget):
    """
    Start menu

    .. versionadded:: 0.4
    """

    def __init__(self,  application, surface_manager):
        """
        Initialises start menu

        :param application: instance of currently running application
        :type application: Application
        """
        super(StartMenuWidget, self).__init__()

        self.application = application
        self.surface_manager = surface_manager

        self.set_layout()

    def set_layout(self):
        """
        Set layout of this screen
        """
        self.setSizePolicy(QSizePolicy(
                                       QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))

        self.width = 800
        self.height = 600

        button = QPushButton('New game', self)
        button.resize(button .sizeHint())
        button.move(325, 200)

        button = QPushButton('Load game', self)
        button.resize(button .sizeHint())
        button.move(325, 250)

        button = QPushButton('Options', self)
        button.resize(button .sizeHint())
        button.move(325, 300)

        button = QPushButton('Quit', self)
        button.clicked.connect(PyQt4.QtCore.QCoreApplication.instance().quit)
        button.resize(button .sizeHint())
        button.move(325, 350)

    def __start_new_game(self):
        """
        Start a new game
        """
        self.logger.info('starting a new game')

        newWindow = herculeum.gui.windows.StartNewGameWindow(self.application, self.surface_manager)
        newWindow.main_loop()

        self.application.world.player = newWindow.character
        self.application.world.end_condition = 0

        self.application.change_state('game window')

    def __options(self):
        """
        Display options
        """
        self.application.change_state('options menu')
