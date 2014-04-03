# -*- coding: utf-8 -*-

#   Copyright 2010-2014 Tuukka Turto
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
Module for curses user interface
"""
import curses

from herculeum.ui.controllers import StartGameController
from herculeum.ui.text.main_window import MainWindow


class CursesUserInterface():
    """
    Class for curses user interface

    .. versionadded:: 0.9
    """
    def __init__(self, application):
        """
        Default constructor
        """
        super().__init__()

        self.application = application
        self.splash_screen = None

        self.curses = curses.initscr()

        if curses.has_colors():
            curses.start_color()

        self.screen = self.curses.subwin(24, 80, 0, 0)

        self.screen.refresh()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

    def show_splash_screen(self):
        """
        Show splash screen
        """
        pass

    def show_main_window(self):
        """
        Show main window
        """
        main_window = MainWindow(self.application,
                                 self.application.surface_manager,
                                 self.screen,
                                 StartGameController(self.application.level_generator_factory,
                                                     self.application.creature_generator,
                                                     self.application.item_generator,
                                                     self.application.config.start_level))

        main_window.show_new_game()
        main_window.show_map_window()

        curses.echo()
        curses.nocbreak()
        curses.curs_set(1)
        curses.endwin()
