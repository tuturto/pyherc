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
Module for main window related functionality
"""
from herculeum.ui.text.start_game import StartGameScreen
from herculeum.ui.text.map import MapScreen
from pyherc.generators.dungeon import DungeonGenerator

class MainWindow(object):
    """
    Main window of the interface

    .. versionadded:: 0.9
    """
    def __init__(self, application, surface_manager, screen):
        """
        Default constructor
        """
        super(MainWindow, self).__init__()

        self.application = application
        self.surface_manager = surface_manager
        self.screen = screen

    def show_new_game(self):
        """
        Show new game dialog
        """
        start_screen = StartGameScreen(self.application.player_generator,
                                       self.application,
                                       self.screen)

        player = start_screen.show()

        #TODO: this is similar to Qt one, refactor
        self.application.world.player = player
        level_generator = self.application.level_generator_factory.get_generator('upper catacombs')

        generator = DungeonGenerator(self.application.creature_generator,
                                     self.application.item_generator,
                                     level_generator)

        generator.generate_dungeon(self.application.world)
        self.application.world.level = self.application.world.dungeon.levels

    def show_map_window(self):
        """
        Show window for playing
        """
        map = MapScreen(model = self.application.world,
                        surface_manager = self.application.surface_manager,
                        action_factory = self.application.action_factory,
                        rng = self.application.rng,
                        rules_engine = self.application.rules_engine,
                        configuration = self.application.config,
                        screen = self.screen)

        self.application.world.register_event_listener(map)
        map.show()
