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
import pyherc.gui.images
import pyherc
import pygame
import pgu.gui
import os
from pyherc.gui.core import Container

class StartMenu(Container):
    """
    Start menu

    .. versionadded:: 0.4
    """

    def __init__(self,  application, surface_manager, **params):
        """
        Initialises start menu

        :param application: instance of currently running application
        :type application: Application
        """
        super(StartMenu, self).__init__(**params)

        self.running = 1
        self.selection = 0
        self.application = application
        self.surface_manager = surface_manager
        self.logger = logging.getLogger('pyherc.gui.windows.StartMenu')

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(application.base_path,
                'music/demetrios_katis_-_the_gathering_of_the_tribes.ogg'))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

        self.set_layout()

    def set_layout(self):
        """
        Set layout of this screen
        """
        bg = pgu.gui.Image(
                self.surface_manager.get_image(
                        pyherc.gui.images.image_start_menu))
        self.add(bg, 0, 0)

        b = pgu.gui.Button("New game", width=150)
        self.add(b, 325, 200)
        b.connect(pgu.gui.CLICK, self.__start_new_game)
        b.focus()

        b = pgu.gui.Button("Load game", width=150)
        self.add(b, 325, 250)

        b = pgu.gui.Button("Options", width=150)
        self.add(b, 325, 300)
        b.connect(pgu.gui.CLICK, self.__options)

        b = pgu.gui.Button("Quit", width=150)
        self.add(b, 325, 350)
        b.connect(pgu.gui.CLICK, self.__quit_game)

    def __start_new_game(self):
        """
        Start a new game
        """
        self.logger.info('starting a new game')

        pygame.mixer.music.fadeout(1000)

        newWindow = pyherc.gui.windows.StartNewGameWindow(self.application, self.surface_manager)
        newWindow.main_loop()

        self.application.world.player = newWindow.character
        self.application.world.end_condition = 0

        self.application.change_state('game window')

        # newWindow = pyherc.gui.windows.OldGameWindow(self.application, self.screen, self.surface_manager)
        # newWindow.main_loop()
        #  self.logger.info('game finished')
        # if self.application.running:
        #    endResult = pyherc.rules.ending.check_result(self.application.world)
        #    dialog = pyherc.gui.dialogs.EndScreen(self.application, self.screen, self.surface_manager)
        #    dialog.show(endResult)

        # self.repaint()
        # self.application.change_state('game window')

        #newWindow = pyherc.gui.windows.GameWindow(self.application, self.screen, self.surface_manager)
        #newWindow.main_loop()
        #self.logger.info('game finished')
        #if self.application.running:
        #    endResult = pyherc.rules.ending.check_result(self.application.world)
        #    dialog = pyherc.gui.dialogs.EndScreen(self.application, self.screen, self.surface_manager)
        #    dialog.show(endResult)

        #self.repaint()

    def __quit_game(self):
        """
        Quit game and exit
        """
        #pylint: disable=E1103
        self.get_toplevel().quit()

    def __options(self):
        """
        Display options
        """
        self.application.change_state('options menu')

