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
Module for various windows used in game
"""

import pygame
import logging
import pyherc.gui.images
import pyherc.rules.character
import pyherc.data.model
import pyherc.data.tiles
import pyherc.rules.items
import pyherc.rules.ending
import pyherc.generators.dungeon
import pyherc.rules.tables
import pyherc.gui.startmenu
import pgu.gui.app
from pyherc.gui.dialogs import Inventory
from pyherc.aspects import Logged
from pyherc.rules.los import get_fov_matrix
from pygame.locals import K_ESCAPE, K_PERIOD
from pygame.locals import K_d, K_w, K_r, K_q,  K_i
from pygame.locals import K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9

from pyherc.gui.options import OptionsMenu
from pyherc.gui.startmenu import StartMenu
from pyherc.gui.gamewindow import GameWindow
from pyherc.gui.inventory import InventoryWindow

class MainWindow(pgu.gui.app.App):
    """
    Main window of the game
    """
    logged = Logged()

    @logged
    def __init__(self,  application, base_path, surface_manager, theme=None, **params):
        """
        Initialises the main window

        Args:
            application: instance of currently running application
            base_path: location of resources directory
            surface_manager: optional SurfaceManger to use for loading resources
        """
        super(MainWindow, self).__init__(theme, **params)
        self.logger = logging.getLogger('pyherc.gui.windows.MainWindow')
        self.logger.info('Initialising MainWindow')
        self.display = None
        self.application = application
        pygame.init()
        self.width = application.config.resolution[0]
        self.height = application.config.resolution[1]
        pygame.display.set_caption(application.config.caption)

        self.surface_manager = surface_manager
        self.state = None

    @logged
    def change_state(self, state):
        """
        Change state of the gui

        Args:
            state: String specifying which state to display
        """
        self.state = state
        if state == 'options menu':
            mode = OptionsMenu(self.application,
                               self.surface_manager)
        elif state == 'start menu':
            mode = StartMenu(self.application,
                             self.surface_manager)
        elif state == 'game window':
            mode = GameWindow(self.application,
                              self.surface_manager)
        elif state == 'inventory':
            mode = InventoryWindow(self.application,
                                   self.surface_manager)
        if state != None:
            self.init(widget = mode)

    def loop(self):
        """
        Performs one iteration of the PGU application loop, which
        processes events and update the pygame display.
        """
        super(MainWindow, self).loop()
        if self.state == 'game window':
            model = self.application.world
            player = model.player

            if player.tick > 0:
                creature = model.get_next_creature()

                if creature != model.player:
                    if self.application.world.player.level != None:
                        creature.act(self.application.world)

class StartNewGameWindow:
    """
    Window that is displayed when player starts a new game
    """
    def __init__(self,  application, surface_manager):
        self.logger = logging.getLogger('pyherc.gui.windows.StartNewGameWindow')

        self.running = 1
        self.application = application
        self.surface_manager = surface_manager
        self.character = None

    def main_loop(self):
        """
        Main loop of the window
        """
        self.__generate_new_game()

    def __generate_new_game(self):
        """
        Generate a new game
        """
        self.character = pyherc.rules.character.create_character('human',
                                                'fighter',
                                                self.application.world,
                                                self.application.action_factory,
                                                self.application.rng)
        self.application.world.player = self.character

        level_generator = self.application.level_generator_factory.get_generator('upper catacombs')

        generator = pyherc.generators.dungeon.DungeonGenerator(
                                self.application.creature_generator,
                                self.application.item_generator,
                                level_generator)

        generator.generate_dungeon(self.application.world)
        self.character.level = self.application.world.dungeon.levels
        self.character.name = 'Adventurer'
