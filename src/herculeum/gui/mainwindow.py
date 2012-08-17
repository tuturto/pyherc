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
Module for main window related functionality
"""

from PyQt4.QtGui import QMainWindow, QAction, QIcon, QVBoxLayout, QWorkspace
from PyQt4.QtCore import SIGNAL
import PyQt4.QtGui
import os

from herculeum.gui.startgame import StartGameWidget

class MainWindow(QMainWindow):
    """
    Class for displaying main window

    .. versionadded:: 0.5
    """
    def __init__(self, application, surface_manager):
        """
        Default constructor
        """
        super(MainWindow, self).__init__()

        self.application = application
        self.surface_manager = surface_manager

        self.__set_layout()

    def __set_layout(self):

        #surface manager?
        new_action = QAction(QIcon(os.path.join(self.application.base_path,
                                                'cycle.png')),
                             '&New game',
                             self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Start a new game')

        exit_action = QAction(QIcon(os.path.join(self.application.base_path,
                                                'wooden-door.png')),
                             '&Quit',
                             self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Quit game')
        exit_action.triggered.connect(PyQt4.QtGui.qApp.quit)

        inventory_action = QAction(QIcon(os.path.join(self.application.base_path,
                                                      'swap-bag.png')),
                                         'Inventory',
                                         self)
        inventory_action.setShortcut('Ctrl+I')
        inventory_action.setStatusTip('Show inventory')

        character_action = QAction(QIcon(os.path.join(self.application.base_path,
                                                      'strong.png')),
                                         'Character',
                                         self)
        character_action.setShortcut('Ctrl+C')
        character_action.setStatusTip('Show character')

        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.addAction(inventory_action)
        self.toolbar.addAction(character_action)

        self.statusBar()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(exit_action)

        actions_menu = menubar.addMenu('&Actions')
        actions_menu.addAction(inventory_action)
        actions_menu.addAction(character_action)

        self.ws = QWorkspace(self)
        self.ws.setScrollBarsEnabled(True)
        self.setCentralWidget(self.ws)

        self.connect(new_action,
                     SIGNAL("triggered()"),
                     self.__show_new_game)

        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('Herculeum')
        self.setWindowIcon(QIcon(os.path.join(self.application.base_path,
                                                'rune-stone.png')))
        self.show()

    def __show_new_game(self):
        """
        Show new game dialog
        """
        start_dialog = StartGameWidget(parent = self,
                                       application = self.application,
                                       surface_manager = self.surface_manager)

        start_dialog.open()
