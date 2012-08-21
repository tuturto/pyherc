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

from PyQt4.QtGui import QMainWindow, QAction, QIcon, QVBoxLayout, QMdiArea
from PyQt4.QtGui import QDialog, QPushButton, QWorkspace
from PyQt4.QtCore import SIGNAL, Qt
import PyQt4.QtGui
import os
import pyherc.rules.character

from herculeum.gui.startgame import StartGameWidget
from herculeum.gui.map import PlayMapWindow
from herculeum.gui.eventdisplay import EventMessageDockWidget
from herculeum.gui.inventory import InventoryDockWidget
from herculeum.config import tiles

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

        new_action = QAction(QIcon(self.surface_manager.get_icon(tiles.ICON_NEW_GAME)),
                             '&New game',
                             self)
        new_action.setShortcut('Ctrl+N')
        new_action.setStatusTip('Start a new game')

        exit_action = QAction(QIcon(self.surface_manager.get_icon(tiles.ICON_QUIT_GAME)),
                             '&Quit',
                             self)

        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Quit game')
        exit_action.triggered.connect(PyQt4.QtGui.qApp.quit)

        inventory_action = QAction(QIcon(self.surface_manager.get_icon(tiles.ICON_INVENTORY)),
                                         'Inventory',
                                         self)
        inventory_action.setShortcut('Ctrl+I')
        inventory_action.setStatusTip('Show inventory')
        inventory_action.triggered.connect(self.__show_inventory)

        character_action = QAction(QIcon(self.surface_manager.get_icon(tiles.ICON_CHARACTER)),
                                         'Character',
                                         self)
        character_action.setShortcut('Ctrl+C')
        character_action.setStatusTip('Show character')

        toolbar = self.addToolBar('Actions')
        toolbar.addAction(inventory_action)
        toolbar.addAction(character_action)

        self.statusBar()

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(exit_action)

        actions_menu = menubar.addMenu('&Actions')
        actions_menu.addAction(inventory_action)
        actions_menu.addAction(character_action)

        self.mdi_area = QMdiArea(self)
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdi_area)

        self.connect(new_action,
                     SIGNAL("triggered()"),
                     self.__show_new_game)

        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('Herculeum')
        self.setWindowIcon(QIcon(self.surface_manager.get_icon(tiles.ICON_HERCULEUM)))
        self.show()

    def __show_new_game(self):
        """
        Show new game dialog
        """
        start_dialog = StartGameWidget(parent = self,
                                       application = self.application,
                                       surface_manager = self.surface_manager)

        result = start_dialog.exec_()

        if result == QDialog.Accepted:
            self.application.world.player = start_dialog.player_character

            level_generator = self.application.level_generator_factory.get_generator('upper catacombs')

            generator = pyherc.generators.dungeon.DungeonGenerator(
                                self.application.creature_generator,
                                self.application.item_generator,
                                level_generator)

            generator.generate_dungeon(self.application.world)
            self.application.world.level = self.application.world.dungeon.levels

            self.__show_map_window()
            self.__show_message_window(self.application.world.player)

    def __show_map_window(self):
        """
        Show map window
        """
        map_window = PlayMapWindow(parent = self.mdi_area,
                                   model = self.application.world,
                                   surface_manager = self.surface_manager,
                                   action_factory = self.application.action_factory,
                                   rng = self.application.rng)
        map_window.show()

    def __show_message_window(self, character):
        """
        Show message display

        :param character: character which events to display
        :type character: Character
        """
        messages_display = EventMessageDockWidget(self, character)

        self.addDockWidget(Qt.BottomDockWidgetArea,
                           messages_display)


    def __show_inventory(self):
        """
        Show inventory
        """
        inventory_display = InventoryDockWidget(self.surface_manager,
                                                self.application.world.player,
                                                self)

        self.addDockWidget(Qt.LeftDockWidgetArea,
                           inventory_display)
