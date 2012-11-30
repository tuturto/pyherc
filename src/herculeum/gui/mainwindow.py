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
from herculeum.gui.menu import MenuDialog
from herculeum.config import tiles

from pyherc.generators import CreatureConfiguration, CreatureGenerator
from random import Random

class MainWindow(QMainWindow):
    """
    Class for displaying main window

    .. versionadded:: 0.5
    """
    def __init__(self, application, surface_manager, parent, flags):
        """
        Default constructor
        """
        super(MainWindow, self).__init__(parent, flags)

        self.application = application
        self.surface_manager = surface_manager

        self.__set_layout()

    def show_help(self):
        self.application.help.show_help('test')

    def __set_layout(self):

        exit_action = QAction(QIcon(':exit-game.png'),
                             '&Quit',
                             self)

        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Quit game')
        exit_action.triggered.connect(PyQt4.QtGui.qApp.quit)

        inventory_action = QAction(QIcon(':inventory.png'),
                                         'Inventory',
                                         self)
        inventory_action.setShortcut('Ctrl+I')
        inventory_action.setStatusTip('Show inventory')
        inventory_action.triggered.connect(self.__show_menu)

        character_action = QAction(QIcon(':character.png'),
                                         'Character',
                                         self)
        character_action.setShortcut('Ctrl+C')
        character_action.setStatusTip('Show character')

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)

        self.map_window = PlayMapWindow(parent = None,
                                        model = self.application.world,
                                        surface_manager = self.surface_manager,
                                        action_factory = self.application.action_factory,
                                        rng = self.application.rng,
                                        rules_engine = self.application.rules_engine)
        self.setCentralWidget(self.map_window)

        self.map_window.MenuRequested.connect(self.__show_menu)

        self.setGeometry(50, 50, 800, 600)
        self.setWindowTitle('Herculeum')
        self.setWindowIcon(QIcon(':rune-stone.png'))
        self.showMaximized()

    def show_new_game(self):
        """
        Show new game dialog
        """
        config = {}

        config['Warrior'] = CreatureConfiguration(
                                name = 'Warrior',
                                body = 8,
                                finesse = 8,
                                mind = 5,
                                hp = 9,
                                speed = 1,
                                icons = 300,
                                attack = 1,
                                description = 'Stout warrior')

        app = self.application

        generator = CreatureGenerator(configuration = config,
                                      model = app.world,
                                      item_generator = app.item_generator,
                                      rng = app.rng)

        start_dialog = StartGameWidget(generator = generator,
                                       parent = self,
                                       application = self.application,
                                       surface_manager = self.surface_manager,
                                       flags = Qt.Dialog | Qt.CustomizeWindowHint)

        result = start_dialog.exec_()

        if result == QDialog.Accepted:
            player = start_dialog.player_character
            self.application.world.player = player
            player.register_for_updates(self.map_window.hit_points_widget)
            self.map_window.hit_points_widget.show_hit_points(player)
            level_generator = self.application.level_generator_factory.get_generator('upper catacombs')

            generator = pyherc.generators.dungeon.DungeonGenerator(
                                self.application.creature_generator,
                                self.application.item_generator,
                                level_generator)

            generator.generate_dungeon(self.application.world)
            self.application.world.level = self.application.world.dungeon.levels

            self.__show_map_window()

    def __show_map_window(self):
        """
        Show map window
        """
        self.map_window.construct_scene()

    def __show_message_window(self, character):
        """
        Show message display

        :param character: character which events to display
        :type character: Character
        """
        messages_display = EventMessageDockWidget(self, character)

        self.addDockWidget(Qt.BottomDockWidgetArea,
                           messages_display)


    def __show_menu(self):
        """
        Show menu
        """
        menu_dialog = MenuDialog(self.surface_manager,
                                 self.application.world.player,
                                 self.application.action_factory,
                                 self,
                                 Qt.Dialog | Qt.CustomizeWindowHint)
        menu_dialog.exec_()
