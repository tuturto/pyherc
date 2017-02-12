# -*- coding: utf-8 -*-

# Copyright (c) 2010-2017 Tuukka Turto
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for main window related functionality
"""
from herculeum.ui.text.map import MapScreen
from herculeum.ui.text.start_game import StartGameScreen


class MainWindow():
    """
    Main window of the interface

    .. versionadded:: 0.9
    """
    def __init__(self, application, surface_manager, screen,
                 controller):
        """
        Default constructor
        """
        super(MainWindow, self).__init__()

        self.application = application
        self.surface_manager = surface_manager
        self.screen = screen
        self.controller = controller

    def show_new_game(self):
        """
        Show new game dialog
        """
        start_screen = StartGameScreen(self.application.player_generator,
                                       self.application,
                                       self.screen)

        player = start_screen.show()

        self.controller.setup_world(self.application.world,
                                    player)

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
